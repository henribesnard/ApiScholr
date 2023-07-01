from rest_framework import serializers
from .models import Schoolclass, Course
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

User = get_user_model()

class SchoolclassSerializer(serializers.ModelSerializer):
    principal_teacher = serializers.PrimaryKeyRelatedField(queryset=User.objects.filter(roles__name='TEACHER'), required=False)
    students = serializers.PrimaryKeyRelatedField(queryset=User.objects.filter(roles__name='STUDENT'), many=True, required=False)
    establishment = serializers.PrimaryKeyRelatedField(read_only=True, required=False)
    
    class Meta:
        model = Schoolclass
        fields = '__all__'
        
    def validate_principal_teacher(self, principal_teacher):
        request_user = self.context['request'].user
        if principal_teacher and not principal_teacher.establishments.filter(id=request_user.current_establishment.id).exists():
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
    schoolclasses = serializers.PrimaryKeyRelatedField(queryset=Schoolclass.objects.all(), many=True)  # Ajouté pour gérer plusieurs classes
    
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

    def validate_schoolclasses(self, schoolclasses):  
        request_user = self.context['request'].user
        for schoolclass in schoolclasses:
            if schoolclass.establishment != request_user.current_establishment:
                raise serializers.ValidationError(_("All classes must belong to your establishment."))
        return schoolclasses

    def create(self, validated_data):
        teachers_data = validated_data.pop('teachers')
        schoolclasses_data = validated_data.pop('schoolclasses')
        request_user = self.context['request'].user
        course = Course.objects.create(**validated_data, created_by=request_user)
        course.teachers.set(teachers_data)
        course.schoolclasses.set(schoolclasses_data)
        return course




class SchoolclassUpdateSerializer(serializers.ModelSerializer):
    students = serializers.PrimaryKeyRelatedField(queryset=User.objects.filter(roles__name='STUDENT'), many=True)
    principal_teacher = serializers.PrimaryKeyRelatedField(queryset=User.objects.none())  # Initialise avec un queryset vide

    class Meta:
        model = Schoolclass
        fields = ['name', 'students', 'principal_teacher', 'is_active']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request_user = self.context['request'].user
        # Mise à jour du queryset pour principal_teacher avec les enseignants de l'établissement de l'utilisateur courant
        self.fields['principal_teacher'].queryset = User.objects.filter(establishments=request_user.current_establishment, roles__name='TEACHER')

    def validate_students(self, students):
        request_user = self.context['request'].user
        for student in students:
            if not student.establishments.filter(id=request_user.current_establishment.id).exists():
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
    schoolclasses = serializers.PrimaryKeyRelatedField(  # Ajouté pour gérer plusieurs classes
        queryset=Schoolclass.objects.all(),
        many=True
    )

    class Meta:
        model = Course
        fields = ['name', 'schoolclasses', 'subject', 'teachers', 'description', 'is_active']  # Modifié pour gérer plusieurs classes

    def validate(self, attrs):
        teachers = attrs.get('teachers')
        user = self.context['request'].user
        for teacher in teachers:
            if not teacher.establishments.filter(id=user.current_establishment.id).exists():
                raise serializers.ValidationError(_("All teachers must be in the same establishment as the user."))
        schoolclasses = attrs.get('schoolclasses')  # Ajouté pour gérer plusieurs classes
        for schoolclass in schoolclasses:  # Ajouté pour gérer plusieurs classes
            if schoolclass.establishment != user.current_establishment:
                raise serializers.ValidationError(_("All classes must be in the same establishment as the user."))
        return attrs
