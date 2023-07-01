from django.db import models
from django.utils.translation import gettext_lazy as _
from etabs.models import Establishment
from django.conf import settings
from django.core.exceptions import ValidationError

class Schoolclass(models.Model):
    LEVELS = (
        ('MAT1', _('Maternelle 1')),
        ('MAT2', _('Maternelle 2')),
        ('C1', _('Primaire C1')),
        ('CP', _('Primaire CP')),
        ('CE1', _('Primaire CE1')),
        ('CE2', _('Primaire CE2')),
        ('CM1', _('Primaire CM1')),
        ('CM2', _('Primaire CM2')),
        ('6EME', _('Secondaire 6eme')),
        ('5EME', _('Secondaire 5eme')),
        ('4EME', _('Secondaire 4eme')),
        ('3EME', _('Secondaire 3eme')),
        ('2ND', _('Secondaire 2nd')),
        ('1ERE', _('Secondaire 1ere')),
        ('TERM', _('Secondaire Terminal')),
        ('L1', _('Universitaire Licence 1')),
        ('L2', _('Universitaire Licence 2')),
        ('L3', _('Universitaire Licence 3')),
        ('M1', _('Universitaire Master 1')),
        ('M2', _('Universitaire Master 2')),
        ('PHD', _('Doctorat')),

    )

    name = models.CharField(_('Name'), max_length=255)
    establishment = models.ForeignKey(Establishment, on_delete=models.CASCADE, verbose_name=_('Establishment'))
    students = models.ManyToManyField(settings.AUTH_USER_MODEL, limit_choices_to={'roles__name': 'Student'}, related_name='student_classes', verbose_name=_('Students'))
    principal_teacher = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, limit_choices_to={'roles__name': 'Teacher'}, on_delete=models.SET_NULL, related_name='principal_teacher_classes', verbose_name=_('Principal teacher'))
    level = models.CharField(_('Level'), max_length=30, choices=LEVELS)
    is_active = models.BooleanField(_('Active'), default=True)
    # champs pour le suivi des modifications
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Creation date'))
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='created_classes', null=True, blank=True, on_delete=models.SET_NULL, verbose_name=_('Created by'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Update date'))
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='updated_classes', null=True, blank=True, on_delete=models.SET_NULL, verbose_name=_('Updated by'))

    class Meta:
        verbose_name = _('Class')
        verbose_name_plural = _('Classes')
        unique_together = (('name', 'establishment'),)

    def clean(self):
     for student in self.students.all():
        if 'STUDENT' not in [role.name for role in student.roles.all()]:
            raise ValidationError("Only students can be assigned to Schoolclass ")

    def __str__(self):
        return self.name


class Course(models.Model):
    SUBJECTS = (
        ('MATH', _('Mathématiques')),
        ('PHYS', _('Physique')),
        ('CHIM', _('Chimie')),
        ('BIO', _('Biologie')),
        ('HIST', _('Histoire')),
        ('GEO', _('Géographie')),
        ('FR', _('Français')),
        ('ENG', _('Anglais')),
        ('PHILO', _('Philosophie')),
        ('ART', _('Arts')),
        ('MUS', _('Musique')),
        ('PE', _('Education Physique')),
        ('IT', _('Informatique')),
        ('ECO', _('Economie')),
    )

    name = models.CharField(_('Name'), max_length=100)
    schoolclasses = models.ManyToManyField(Schoolclass, verbose_name=_('Classes'))
    subject = models.CharField(_('Subject'), max_length=20, choices=SUBJECTS)
    coefficient = models.IntegerField(_('Coefficient'), default=1)
    teachers = models.ManyToManyField(settings.AUTH_USER_MODEL, limit_choices_to={'roles__name': 'Teacher'}, blank=True, verbose_name=_('Teachers'))
    description = models.TextField(_('Description'), blank=True, null=True)
    is_active = models.BooleanField(_('Active'), default=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Creation date'))
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='created_courses', null=True, blank=True, on_delete=models.SET_NULL, verbose_name=_('Created by'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Update date'))
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='updated_courses', null=True, blank=True, on_delete=models.SET_NULL, verbose_name=_('Updated by'))

    class Meta:
       verbose_name = _('Course')
       verbose_name_plural = _('Courses')
       
    def clean(self):
     for teacher in self.teachers.all():
        if any(role.name != 'TEACHER' for role in teacher.roles.all()):
            raise ValidationError("Only users with the 'Teacher' role can be assigned to a course")


    def __str__(self):
       return self.name

