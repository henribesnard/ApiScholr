from decimal import Decimal
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator

# Évaluation
class Assessment(models.Model):
    EVALUATION_TYPES = (
        ('INTERROGATION', _('Interrogation')),
        ('PARTIEL', _('Partiel')),
        ('DEVOIR', _('Devoir')),
        ('EXAMEN_FINAL', _('Examen final')),
        ('EVALUATION_CONTINUE', _('Évaluation continue')),
    )

    id = models.AutoField(primary_key=True)
    name = models.CharField(_('Name'), max_length=200)
    description = models.TextField(_('Description'), blank=True, null=True)
    date = models.DateField(_('Date'))
    total_points = models.DecimalField(_('Total Points'), max_digits=5, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    type = models.CharField(_('Type'), max_length=25, choices=EVALUATION_TYPES, default='INTERROGATION')
    course = models.ForeignKey('classes.Course', on_delete=models.CASCADE, related_name='assessments')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="created_assessments")
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="updated_assessments")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Assessment')
        verbose_name_plural = _('Assessments')

    def __str__(self):
        return self.name

# Notes
class Grade(models.Model):
    id = models.AutoField(primary_key=True)
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_('Student'))
    assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE, verbose_name=_('Assessment'))
    points_obtained = models.DecimalField(_("Points Obtained"), max_digits=6, decimal_places=2)
    comment = models.TextField(_('Comment'), blank=True, null=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="created_grades")
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="updated_grades")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Grade')
        verbose_name_plural = _('Grades')

    def __str__(self):
        return f"{self.student} - {self.assessment} - {self.points_obtained}"
