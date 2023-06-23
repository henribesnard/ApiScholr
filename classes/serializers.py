from rest_framework import serializers
from .models import Schoolclass, Course
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

User = get_user_model()

class SchoolclassSerializer(serializers.ModelSerializer):
    principal_teacher = serializers.PrimaryKeyRelatedField(queryset=User.objects.filter(roles__name='TEACHER'))
    students = serializers.PrimaryKeyRelatedField(queryset=User.objects.filter(roles__name='STUDENT'), many=True)
    establishment = serializers.PrimaryKeyRelatedField(read_only=True, required=False)
    
    class Meta:
        model = Schoolclass
        fields = '__all__'
        
    def validate_principal_teacher(self, principal_teacher):
        request_user = self.context['request'].user
        if not principal_teacher.establishments.filter(id=request_user.current_establishment.id).exists():
            raise serializers.ValidationError(_("The principal teacher must belong to your establishment."))
        return principal_teacher
    
    def validate_students(self, students):
        request_user = self.context['request'].user
        for student in students:
          if not student.establishments.filter(id=request_user.current_establishment.id).exists():
            raise serializers.ValidationError(_("All students must belong to your establishment."))
        return students


    def create(self, validated_data):
        request_user = self.context['request'].user
        validated_data['establishment'] = request_user.current_establishment
        validated_data['created_by'] = request_user
        return super().create(validated_data)


class CourseSerializer(serializers.ModelSerializer):
    teachers = serializers.PrimaryKeyRelatedField(queryset=User.objects.filter(roles__name='TEACHER'), many=True)
    
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
            if not teacher.establishments.filter(id=request_user.current_establishment.id).exists():
                raise serializers.ValidationError(_("All teachers must belong to your establishment."))
        return teachers

    def create(self, validated_data):
        request_user = self.context['request'].user
        schoolclass = validated_data.get('schoolclass')
        if schoolclass.establishment == request_user.current_establishment:
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
        self.fields['principal_teacher'].queryset = User.objects.filter(establishments=request_user.current_establishment, roles__name='TEACHER')

    def validate_students(self, students):
        request_user = self.context['request'].user
        for student in students:
            if student.current_establishment != request_user.current_establishment:
                raise serializers.ValidationError(_("All students must belong to your establishment."))
        return students

    def validate_principal_teacher(self, principal_teacher):
        request_user = self.context['request'].user
        if not principal_teacher.establishments.filter(id=request_user.current_establishment.id).exists():
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
            if not teacher.establishments.filter(id=user.current_establishment.id).exists():
                raise serializers.ValidationError(_("All teachers must be in the same establishment as the user."))
            if attrs.get('schoolclass').establishment != user.current_establishment:
                raise serializers.ValidationError(_("The course must be in the same establishment as the user."))
        return attrs