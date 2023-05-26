from django.contrib import admin
from .models import EstablishmentType, Establishment

@admin.register(Establishment)
class EstablishmentAdmin(admin.ModelAdmin):
    pass

@admin.register(EstablishmentType)
class EstablishmentTypeAdmin(admin.ModelAdmin):
    pass
