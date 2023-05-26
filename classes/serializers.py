from rest_framework import serializers
from .models import Schoolclass, Course
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

User = get_user_model()

class SchoolclassSerializer(serializers.ModelSerializer):
    principal_teacher = serializers.PrimaryKeyRelatedField(queryset=User.objects.filter(roles__name='Teacher'))
    students = serializers.PrimaryKeyRelatedField(queryset=User.objects.filter(roles__name='Student'), many=True)
    
    class Meta:
        model = Schoolclass
        fields = '__all__'
        
    def validate_principal_teacher(self, principal_teacher):
        request_user = self.context['request'].user
        if principal_teacher.establishment != request_user.establishment:
            raise serializers.ValidationError(_("The principal teacher must belong to your establishment."))
        return principal_teacher
    
    def validate_students(self, students):
        request_user = self.context['request'].user
        for student in students:
            if student.establishment != request_user.establishment:
                raise serializers.ValidationError(_("All students must belong to your establishment."))
        return students

    def create(self, validated_data):
        request_user = self.context['request'].user
        validated_data['establishment'] = request_user.establishment
        validated_data['created_by'] = request_user
        return super().create(validated_data)


class CourseSerializer(serializers.ModelSerializer):
    teachers = serializers.PrimaryKeyRelatedField(queryset=User.objects.filter(roles__name='Teacher'), many=True)
    
    class Meta:
        model = Course
        fields = '__all__'
        
    def validate_coefficient(self, coefficient):
        if coefficient <= 0:
            raise serializers.ValidationError(_("Coefficient must be greater than 0."))
        return coefficient

    def validate_teachers(self, teachers):
        request_user = self.context['request'].user
        for teacher in teachers:
            if teacher.establishment != request_user.establishment:
                raise serializers.ValidationError(_("All teachers must belong to your establishment."))
        return teachers

    def create(self, validated_data):
        request_user = self.context['request'].user
        schoolclass = validated_data.get('schoolclass')
        if schoolclass.establishment == request_user.establishment:
            validated_data['created_by'] = request_user
            return super().create(validated_data)
        else:
            raise serializers.ValidationError({"schoolclass": _("This class does not belong to your establishment.")})


class SchoolclassUpdateSerializer(serializers.ModelSerializer):
    students = serializers.PrimaryKeyRelatedField(queryset=User.objects.filter(roles__name='STUDENT'), many=True)
    principal_teacher = serializers.PrimaryKeyRelatedField(queryset=User.objects.none())  # Initialise avec un queryset vide

    class Meta:
        model = Schoolclass
        fields = ['name', 'establishment', 'students', 'principal_teacher', 'level', 'is_active']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request_user = self.context['request'].user
        # Mise à jour du queryset pour principal_teacher avec les enseignants de l'établissement de l'utilisateur courant
        self.fields['principal_teacher'].queryset = User.objects.filter(establishment=request_user.establishment, roles__name='TEACHER')

    def validate_students(self, students):
        request_user = self.context['request'].user
        for student in students:
            if student.establishment != request_user.establishment:
                raise serializers.ValidationError(_("All students must belong to your establishment."))
        return students

    def validate_principal_teacher(self, principal_teacher):
        request_user = self.context['request'].user
        if principal_teacher.establishment != request_user.establishment:
            raise serializers.ValidationError(_("The principal teacher must belong to your establishment."))
        return principal_teacher

class CourseUpdateSerializer(serializers.ModelSerializer):
    teachers = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(roles__name='TEACHER'),
        many=True
    )

    class Meta:
        model = Course
        fields = ['name', 'schoolclass', 'subject', 'teachers', 'description', 'is_active']

    def validate(self, attrs):
        teachers = attrs.get('teachers')
        user = self.context['request'].user
        for teacher in teachers:
            if teacher.establishment != user.establishment:
                raise serializers.ValidationError(_("All teachers must be in the same establishment as the user."))
            if attrs.get('schoolclass').establishment != user.establishment:
                raise serializers.ValidationError(_("The course must be in the same establishment as the user."))
        return attrs