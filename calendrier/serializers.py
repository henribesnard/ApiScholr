from rest_framework import serializers
from .models import Room, Timeslot
from django.utils.translation import gettext_lazy as _

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['id', 'name', 'capacity', 'description', 'establishment']
        read_only_fields = ['establishment'] # L'utilisateur ne peut pas modifier l'établissement 

    def create(self, validated_data):
        # L'établissement est automatiquement celui de l'utilisateur qui ajoute la Room
        validated_data['establishment'] = self.context['request'].user.establishment
        return Room.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.capacity = validated_data.get('capacity', instance.capacity)
        instance.description = validated_data.get('description', instance.description)
        instance.save()
        return instance


class TimeslotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Timeslot
        fields = [
            'id',
            'schoolclass',
            'course',
            'room',
            'start_datetime',
            'end_datetime',
            'created_at',
            'created_by',
            'updated_at',
            'updated_by'
        ]
        read_only_fields = ['created_at', 'created_by', 'updated_at', 'updated_by']

    def validate(self, data):
        """
        Check that start is before end and no overlapping.
        """
        if data['start_datetime'] >= data['end_datetime']:
            raise serializers.ValidationError(_("End datetime must occur after start datetime"))

        schoolclass = data['schoolclass']
        room = data['room']
        start_datetime = data['start_datetime']
        end_datetime = data['end_datetime']

        if not self.check_class_availability(schoolclass, start_datetime, end_datetime):
            raise serializers.ValidationError(_("The selected class is not available during this timeslot"))

        if not self.check_room_availability(room, start_datetime, end_datetime):
            raise serializers.ValidationError(_("The selected room is not available during this timeslot"))

        # Create a temporary Timeslot instance to check overlapping
        temp_timeslot = Timeslot(schoolclass=schoolclass, course=data['course'], room=room,
                                 start_datetime=start_datetime, end_datetime=end_datetime)
        if temp_timeslot.has_overlapping():
            raise serializers.ValidationError(_("The timeslot is overlapping with another timeslot"))

        return data

    def check_class_availability(self, schoolclass, start_datetime, end_datetime):
        overlapping_slots = Timeslot.objects.filter(
            schoolclass=schoolclass,
            start_datetime__lt=end_datetime,
            end_datetime__gt=start_datetime
        ).exclude(pk=self.instance.id if self.instance else None)

        return not overlapping_slots.exists()

    def check_room_availability(self, room, start_datetime, end_datetime):
        overlapping_rooms = Timeslot.objects.filter(
            room=room,
            start_datetime__lt=end_datetime,
            end_datetime__gt=start_datetime
        ).exclude(pk=self.instance.id if self.instance else None)

        return not overlapping_rooms.exists()
