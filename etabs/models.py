from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator


class EstablishmentType(models.Model):
    NAMES = (
        ('PRESCHOOL', _('Preschool')),
        ('PRIMARY', _('Primary')),
        ('MIDDLE_SCHOOL', _('Middle School')),
        ('HIGH_SCHOOL', _('High School')),
        ('UNIVERSITY', _('University')),
        ('INSTITUTE', _('Institute')),
        ('TRAINING_CENTER', _('Training Center')),
    )

    id = models.AutoField(primary_key=True)
    name = models.CharField(_('Name'), max_length=50, choices=NAMES, unique=True)

    class Meta:
        verbose_name = _('Establishment Type')
        verbose_name_plural = _('Establishment Types')

    def __str__(self):
        return self.name


class Establishment(models.Model):
    CATEGORIES = (
        ('PUBLIC', _('Public')),
        ('PRIVATE', _('Private')),
    )

    # Validation for phone number
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message=_("Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    )

    id = models.AutoField(primary_key=True)
    name = models.CharField(_('Name'), max_length=100, unique=True)
    address = models.ForeignKey('users.Address', on_delete=models.SET_NULL, verbose_name=_('address'), null=True, blank=True)
    types = models.ManyToManyField(EstablishmentType, verbose_name=_('Types'))
    category = models.CharField(_('Category'), max_length=50, choices=CATEGORIES)
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True, null=True)
    head = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, limit_choices_to={'roles__name__icontains': 'Head'}, on_delete=models.SET_NULL, related_name='headed_establishments')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Creation date'))
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='created_Establishments', null=True, blank=True, on_delete=models.SET_NULL, verbose_name=_('User who created'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Update date'))
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='updated_Establishments', null=True, blank=True, on_delete=models.SET_NULL, verbose_name=_('User who updated'))
    is_active = models.BooleanField(_('Active'), default=True)

    class Meta:
        verbose_name = _('Establishment')
        verbose_name_plural = _('Establishments')

    def __str__(self):
        return self.name
