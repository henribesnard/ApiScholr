from django.db import models
from django.conf import settings
from classes.models import Schoolclass, Course
from etabs.models import Establishment
from django.utils.translation import gettext_lazy as _

class Room(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(_('Name'), max_length=100)
    capacity = models.IntegerField(_('Capacity'), blank=True, null=True)
    description = models.TextField(_('Description'), blank=True, null=True)
    establishment = models.ForeignKey(Establishment, on_delete=models.CASCADE, verbose_name=_('Establishment'))

    class Meta:
        verbose_name = _('Room')
        verbose_name_plural = _('Rooms')

    def __str__(self):
        return self.name

class Timeslot(models.Model):
    id = models.AutoField(primary_key=True)
    schoolclass = models.ForeignKey(Schoolclass, on_delete=models.CASCADE, verbose_name=_('Class'))
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name=_('Course'), blank=True, null=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, verbose_name=_('Room'), blank=True, null=True)
    start_datetime = models.DateTimeField(_('Start datetime'))
    end_datetime = models.DateTimeField(_('End datetime'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Creation date'))
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='created_timeslots', null=True, blank=True, on_delete=models.SET_NULL, verbose_name=_('Created by'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Update date'))
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='updated_timeslots', null=True, blank=True, on_delete=models.SET_NULL, verbose_name=_('Updated by'))

    class Meta:
        verbose_name = _('Timeslot')
        verbose_name_plural = _('Timeslots')
        unique_together = ('room', 'start_datetime', 'end_datetime')
    
    def has_overlapping(self):
        overlapping_timeslots = Timeslot.objects.filter(
            models.Q(course=self.course) | models.Q(room=self.room),
            start_datetime__lt=self.end_datetime,
            end_datetime__gt=self.start_datetime,
        ).exclude(pk=self.pk)
    
        return overlapping_timeslots.exists()

    def __str__(self):
        return f"{self.schoolclass} - {self.course} - {self.room} - {self.start_datetime} - {self.end_datetime}"
