from rest_framework import serializers
from .models import Assessment, Grade, Performance
from django.utils.translation import gettext_lazy as _

class AssessmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assessment
        fields = '__all__'
        
    def create(self, validated_data):
        request_user = self.context['request'].user
        course = validated_data.get('course')
        if course.created_by.establishment == request_user.establishment:
            validated_data['created_by'] = request_user
            return super().create(validated_data)
        else:
            raise serializers.ValidationError({"course": _("This course does not belong to your establishment.")})

class GradeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Grade
        fields = '__all__'

    def validate(self, attrs):
        request_user = self.context['request'].user
        student = attrs.get('student')
        assessment = attrs.get('assessment')

        if student.establishment != request_user.establishment or assessment.course.schoolclass.establishment != request_user.establishment:
            raise serializers.ValidationError("The student and assessment must belong to your establishment.")

        return attrs

    def create(self, validated_data):
        request_user = self.context['request'].user
        validated_data['created_by'] = request_user
        return super().create(validated_data)

class PerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Performance
        fields = '__all__'
        
    def validate(self, attrs):
        request_user = self.context['request'].user
        if attrs['student'].establishment != request_user.establishment:
            raise serializers.ValidationError({"student": _("The student does not belong to your establishment.")})
        if attrs['assessment'].course.schoolclass.establishment != request_user.establishment:
            raise serializers.ValidationError({"assessment": _("The assessment does not belong to your establishment.")})
        return attrs

    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)
