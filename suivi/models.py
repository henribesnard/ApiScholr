from django.db import models
from django.utils.translation import gettext_lazy as _
from classes.models import Course, Schoolclass
from calendrier.models import Timeslot
from django.conf import settings
from django.core.exceptions import ValidationError
from PIL import Image
from django.db.models import Q


class Attendance(models.Model):
    id = models.AutoField(primary_key=True)
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, limit_choices_to=Q(roles__name='Student'), verbose_name=_('Student'))
    timeslot = models.ForeignKey(Timeslot, on_delete=models.CASCADE, verbose_name=_('Timeslot'))  
    STATUS_CHOICES = [
        ('PRESENT', _('Present')),
        ('ABSENT', _('Absent')),
        ('LATE', _('Late')),
        ('EXCUSED', _('Excused')),
    ]
    status = models.CharField(_('Status'), max_length=10, choices=STATUS_CHOICES, default='PRESENT')
    remarks = models.TextField(_('Remarks'), blank=True, null=True)

    def clean(self):
     if not any(role.name == 'STUDENT' for role in self.student.roles.all()):
        raise ValidationError("Only students can be assigned to attendance records")


    class Meta:
        verbose_name = _('Attendance')
        verbose_name_plural = _('Attendances')
    
    def save(self, *args, **kwargs):
        self.clean()
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.student} - {self.timeslot} - {self.date}"  


class Photo(models.Model):
    id = models.AutoField(primary_key=True)
    image = models.ImageField(upload_to='communicationbook_photos/')

    class Meta:
        verbose_name = _('Photo')
        verbose_name_plural = _('Photos')

    def clean(self):
      img = Image.open(self.image.file)
      if img.size > (500, 500):  # Change to whatever size you want to limit to
        raise ValidationError("Image is too large")
      
    def save(self, *args, **kwargs):
        self.clean()
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.image.url
    
    
class CommunicationBook(models.Model):
    id = models.AutoField(primary_key=True)
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name='communicationbook_entries', limit_choices_to=Q(roles__name='Student'), verbose_name=_('Student'), blank=True, null=True)
    schoolclass = models.ForeignKey(Schoolclass, on_delete=models.CASCADE, verbose_name=_('School Class'), blank=True, null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name=_('Course'), blank=True, null=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, limit_choices_to={'roles__in': ['TEACHER', 'HEAD', 'STAFF']}, verbose_name=_('Author'))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    message = models.TextField(_('Message'))
    homework = models.TextField(_('Homework'), blank=True, null=True)
    parent_seen = models.BooleanField(_('Parent has seen'), default=False)
    parent_acknowledged = models.BooleanField(_('Parent has acknowledged'), default=False)
    photos = models.ManyToManyField(Photo, blank=True)

    def clean(self):
     if not any(role.name in ['TEACHER', 'HEAD', 'STAFF'] for role in self.author.roles.all()):
        raise ValidationError("Only teachers, heads, or staff can be authors")
     if not any(role.name == 'STUDENT' for role in self.student.roles.all()):
        raise ValidationError("Only students can be assigned to attendance records")


    class Meta:
        verbose_name = _('Communication Book')
        verbose_name_plural = _('Communication Books')

    def save(self, *args, **kwargs):
        self.clean()
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.author} - {self.created_at}"
