from django.contrib import admin
from .models import Grade, Assessment

@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    pass

@admin.register(Assessment)
class AssessmentAdmin(admin.ModelAdmin):
    pass
