from django.contrib import admin
from .models import Room, Timeslot

@admin.register(Timeslot)
class TimeslotAdmin(admin.ModelAdmin):
    pass

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    pass