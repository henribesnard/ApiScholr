from rest_framework import serializers
from .models import Attendance, CommunicationBook

class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = ['id', 'name', 'description', 'establishment', 'created_by', 'updated_by']

class CommunicationBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommunicationBook
        fields = ['id', 'student', 'schoolclass', 'course', 'author', 'created_at', 'updated_at', 
                  'message', 'homework', 'parent_seen', 'parent_acknowledged', 'photos']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        request = self.context.get('request', None)
        if request and request.user and request.user.roles.filter(name__in=['HEAD', 'TEACHER', 'STAFF', 'STUDENT']).exists():
            representation['parent_seen'] = {'read_only': True, 'value': instance.parent_seen}
            representation['parent_acknowledged'] = {'read_only': True, 'value': instance.parent_acknowledged}
        return representation

class ParentCommunicationBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommunicationBook
        fields = ['id', 'student', 'schoolclass', 'course', 'author', 'created_at', 'updated_at', 'message', 'homework', 'parent_seen', 'parent_acknowledged', 'photos']
        read_only_fields = ['id', 'student', 'schoolclass', 'course', 'author', 'created_at', 'updated_at', 'message', 'homework', 'photos']


class StudentCommunicationBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommunicationBook
        fields = ['id', 'student', 'schoolclass', 'course', 'author', 'created_at', 'updated_at', 'message', 'homework', 'parent_seen', 'parent_acknowledged', 'photos']