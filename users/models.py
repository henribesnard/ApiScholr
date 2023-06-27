from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.contrib.auth.hashers import make_password, is_password_usable


class Address(models.Model):
    street_number = models.CharField(_('street_number'),max_length=10, null=True, blank=True)
    street_name = models.CharField(_('street_name'),max_length=255, null=True, blank=True)
    postal_code = models.CharField(_('postal_code'),max_length=20, null=True, blank=True)
    city = models.CharField(_('city'),max_length=100)
    department = models.CharField(_('department'),max_length=100, null=True, blank=True)
    country = models.CharField(_('country'),max_length=100)

    def __str__(self):
        return f"{self.street_number} {self.street_name}, {self.postal_code} {self.city}, {self.country}"

class Role(models.Model):
    ROLE_CHOICES = [
        ('HEAD', _('Head of Establishment')),
        ('STAFF', _('Staff')),
        ('TEACHER', _('Teacher')),
        ('PARENT', _('Parent')),
        ('STUDENT', _('Student')),
    ]

    name = models.CharField(_('Name'), max_length=20, choices=ROLE_CHOICES, unique=True)

    def __str__(self):
        return self.name

class User(AbstractUser):
    roles = models.ManyToManyField(Role, blank=True)
    establishments = models.ManyToManyField('etabs.Establishment', blank=True, verbose_name=_('Establishments'))
    current_establishment = models.ForeignKey('etabs.Establishment', related_name='users_with_current', on_delete=models.SET_NULL, verbose_name=_('Current Establishment'), blank=True, null=True)
    children = models.ManyToManyField('self', verbose_name=_('Children'), blank=True,limit_choices_to=Q(roles__name='Student'), symmetrical=False)
    is_principal_teacher = models.BooleanField(_('Principal Teacher'), default=False)
    position = models.CharField(_('Position'), max_length=200, blank=True, null=True)
    profile_picture = models.ImageField(_('Profile picture'), upload_to='profile_pictures/', blank=True, null=True)
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Creation date'))
    created_by = models.ForeignKey('self', related_name='created_users', null=True, blank=True, on_delete=models.SET_NULL, verbose_name=_('User who created'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Update date'))
    updated_by = models.ForeignKey('self', related_name='updated_users', null=True, blank=True, on_delete=models.SET_NULL, verbose_name=_('User who updated'))

    def clean(self):
     if self.pk:
      for child in self.children.all():
        if any(role.name != 'STUDENT' for role in child.roles.all()):
            raise ValidationError("Only students can be assigned as children")

    def save(self, *args, **kwargs):
        if self.pk is None:
            if not is_password_usable(self.password):
                self.password = make_password(self.password)
        else:
            original_user = User.objects.get(pk=self.pk)
            if self.password != original_user.password:
                if not is_password_usable(self.password):
                    self.password = make_password(self.password)

        super().save(*args, **kwargs)

    def __str__(self):
       return f"{self.first_name} {self.last_name}"

