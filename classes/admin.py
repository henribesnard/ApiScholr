from django.contrib import admin
from .models import Schoolclass, Course

@admin.register(Schoolclass)
class SchoolclassAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'principal_teacher', 'level','establishment', 'is_active'] 
    readonly_fields = ('id',)
    fields = ['id', 'name', 'principal_teacher', 'students', 'level', 'establishment', 'is_active'] 


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'subject', 'description'] 
    readonly_fields = ('id',)
    