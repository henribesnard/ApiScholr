from django.contrib import admin
from .models import Attendance, CommunicationBook, Photo

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    pass


@admin.register(CommunicationBook)
class CommunicationBookAdmin(admin.ModelAdmin):
    pass

@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    pass