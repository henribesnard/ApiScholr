from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Role, Address
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
import string, secrets

User = get_user_model()

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        credentials = {
            'username': '',
            'password': attrs.get('password')
        }

        user_model = get_user_model()

        users = user_model.objects.filter(email=attrs.get('username'))
        if users.exists():
            credentials['username'] = users.first().username
        else:
            credentials['username'] = attrs.get('username')

        return super().validate(credentials)



class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['street_number', 'street_name', 'postal_code', 'city', 'department', 'country']


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    roles = RoleSerializer(many=True, read_only=True)
    address = AddressSerializer(read_only=True)

    class Meta:
        model = User
        fields = '__all__'

class UserCreateSerializer(serializers.ModelSerializer):
    username = serializers.CharField(read_only=True)
    email = serializers.EmailField(required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    roles = serializers.SlugRelatedField(
        many=True,
        slug_field='name',
        queryset=Role.objects.all(),
        required=False
    )
    address = AddressSerializer()

    class Meta:
        model = User
        exclude = ['password']

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(_("User with this Email already exists."))
        return value
    @staticmethod
    def generate_temporary_password(length=10):
        if length < 10:
            raise ValueError("Password length should be at least 10")

        # Création de différents ensembles de caractères
        uppercase_letters = string.ascii_uppercase
        lowercase_letters = string.ascii_lowercase
        digits = string.digits
        special_characters = string.punctuation

        # Sélection aléatoire d'au moins un caractère de chaque ensemble
        password = [
            secrets.choice(uppercase_letters),
            secrets.choice(lowercase_letters),
            secrets.choice(digits),
            secrets.choice(special_characters)
        ]

        # Compléter le mot de passe avec des caractères aléatoires
        for i in range(length - 4):
            password.append(secrets.choice(uppercase_letters + lowercase_letters + digits + special_characters))

        # Mélanger les caractères pour obtenir un mot de passe complexe
        secrets.SystemRandom().shuffle(password)

        # Convertir la liste de caractères en chaîne
        return ''.join(password)

    @staticmethod
    def generate_username(first_name, last_name):
        base_username = f"{first_name[:1]}{last_name[:5]}".lower()
        username = base_username
        index = 1

        while User.objects.filter(username=username).exists():
            username = f"{base_username}{index}"
            index += 1

        return username

    def create(self, validated_data):
        roles = validated_data.pop('roles', [])

        first_name = validated_data.get('first_name')
        last_name = validated_data.get('last_name')
        username = self.generate_username(first_name, last_name)
        validated_data['username'] = username  # add username to validated_data

        password = self.generate_temporary_password()

        # create address
        address_data = validated_data.pop('address')
        address = Address.objects.create(**address_data)
        validated_data['address'] = address

        try:
            send_mail(
                _('Your new account'),
                _('Your username is {username} and your temporary password is {password}. Please log in and reset your password as soon as possible.').format(username=username, password=password),
                'from@example.com',
                [validated_data.get('email')],
                fail_silently=False,
            )
        except Exception as e:
            raise ValidationError(_("Error sending email: ") + str(e))

        user = User(**validated_data)
        user.set_password(password)
        user.save()

        # assign roles to user
        for role in roles:
            user.roles.add(role)
        user.save()

        return user
    

class UserCreateByHeadStaffSerializer(serializers.ModelSerializer):
    username = serializers.CharField(read_only=True)
    email = serializers.EmailField(required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    is_staff = serializers.BooleanField(default=False)
    roles = serializers.SlugRelatedField(
        many=True,
        slug_field='name',
        queryset=Role.objects.all(),
        write_only=True,
        required=True
    )
    address = AddressSerializer()

    class Meta:
        model = User
        exclude = ['password']

    def validate_roles(self, roles):
        request_user = self.context['request'].user
        if request_user.roles.filter(name='STAFF').exists() and any(role.name in ['HEAD', 'STAFF'] for role in roles):
            raise serializers.ValidationError(_("Staff cannot create users with role Admin, Head, or Staff."))
        elif request_user.roles.filter(name='HEAD').exists():
            raise serializers.ValidationError(_("Head cannot create users with role Admin."))
        return roles

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(_("User with this Email already exists."))
        return value
    
    @staticmethod
    def generate_temporary_password(length=10):
        if length < 10:
            raise ValueError("Password length should be at least 10")

        # Création de différents ensembles de caractères
        uppercase_letters = string.ascii_uppercase
        lowercase_letters = string.ascii_lowercase
        digits = string.digits
        special_characters = string.punctuation

        # Sélection aléatoire d'au moins un caractère de chaque ensemble
        password = [
            secrets.choice(uppercase_letters),
            secrets.choice(lowercase_letters),
            secrets.choice(digits),
            secrets.choice(special_characters)
        ]

        # Compléter le mot de passe avec des caractères aléatoires
        for i in range(length - 4):
            password.append(secrets.choice(uppercase_letters + lowercase_letters + digits + special_characters))

        # Mélanger les caractères pour obtenir un mot de passe complexe
        secrets.SystemRandom().shuffle(password)

        # Convertir la liste de caractères en chaîne
        return ''.join(password)

    @staticmethod
    def generate_username(first_name, last_name):
        base_username = f"{first_name[:1]}{last_name[:5]}".lower()
        username = base_username
        index = 1

        while User.objects.filter(username=username).exists():
            username = f"{base_username}{index}"
            index += 1

        return username

    def create(self, validated_data):
        request_user = self.context['request'].user
        roles = validated_data.pop('roles', [])

        first_name = validated_data.get('first_name')
        last_name = validated_data.get('last_name')
        username = self.generate_username(first_name, last_name)
        validated_data['username'] = username  # add username to validated_data

        password = self.generate_temporary_password()
        print(f'Generated password: {password}')

        # create address
        address_data = validated_data.pop('address')
        address = Address.objects.create(**address_data)
        validated_data['address'] = address

        try:
            send_mail(
                _('Your new account'),
                _('Your username is {username} and your temporary password is {password}. Please log in and reset your password as soon as possible.').format(username=username, password=password),
                'from@example.com',
                [validated_data.get('email')],
                fail_silently=False,
            )
        except Exception as e:
            raise ValidationError(_("Error sending email: ") + str(e))

        user = User(**validated_data, establishment=request_user.establishment, created_by=request_user)
        user.set_password(password)
        user.save()

        # assign roles to user
        for role in roles:
            user.roles.add(role)
        user.save()

        return user

class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True, 'required': False},
        }

    def update(self, instance, validated_data):
        request_user = self.context['request'].user
        user_roles = [role.name for role in request_user.roles.all()]

        if request_user.is_staff or ((instance.establishment == request_user.establishment) and ('HEAD' in user_roles or 'STAFF' in user_roles)):
            validated_data.pop('password', None)  # remove password from validated_data
            return super().update(instance, validated_data)
        
        if set(user_roles).intersection(['TEACHER', 'STUDENT', 'PARENT']) and instance == request_user:
            allowed_fields = ["email", "address", "phone_number", "profile_picture"]
            for field in validated_data:
                if field not in allowed_fields:
                    raise serializers.ValidationError(_(f"You are not allowed to update {field}"))
            validated_data.pop('password', None)  # remove password from validated_data
            return super().update(instance, validated_data)

        raise serializers.ValidationError(_("You are not allowed to update this user"))
