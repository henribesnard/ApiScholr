from rest_framework import serializers
from .models import Establishment, EstablishmentType
from users.serializers import AddressSerializer
from users.models import Address


class EstablishmentTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = EstablishmentType
        fields = '__all__'


class EstablishmentSerializer(serializers.ModelSerializer):
    types = serializers.PrimaryKeyRelatedField(many=True, queryset=EstablishmentType.objects.all())
    address = AddressSerializer()

    class Meta:
        model = Establishment
        fields = '__all__'

    def create(self, validated_data):
        types_data = validated_data.pop('types', [])
        address_data = validated_data.pop('address', {})
        address = Address.objects.create(**address_data)
        establishment = Establishment.objects.create(address=address, **validated_data)

        for type_id in types_data:
            if isinstance(type_id, EstablishmentType):
                type_id = type_id.id
            type_object = EstablishmentType.objects.get(id=type_id)
            establishment.types.add(type_object)

        return establishment

    def update(self, instance, validated_data):
        types_data = validated_data.pop('types', [])
        address_data = validated_data.pop('address', {})
        
        # update address
        instance.address.street_number = address_data.get('street_number', instance.address.street_number)
        instance.address.street_name = address_data.get('street_name', instance.address.street_name)
        instance.address.postal_code = address_data.get('postal_code', instance.address.postal_code)
        instance.address.city = address_data.get('city', instance.address.city)
        instance.address.department = address_data.get('department', instance.address.department)
        instance.address.country = address_data.get('country', instance.address.country)
        instance.address.save()

        # update establishment types
        instance.types.clear()
        for type_id in types_data:
            if isinstance(type_id, EstablishmentType):
                type_id = type_id.id
            type_object = EstablishmentType.objects.get(id=type_id)
            instance.types.add(type_object)

        # update other fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()

        return instance

