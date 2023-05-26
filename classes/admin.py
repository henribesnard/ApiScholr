from django.contrib import admin
from .models import Schoolclass, Course

@admin.register(Schoolclass)
class SchoolclassAdmin(admin.ModelAdmin):
    pass

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    pass