# Generated by Django 4.2.1 on 2023-06-06 20:08

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='children',
            field=models.ManyToManyField(blank=True, limit_choices_to=models.Q(('roles__name', 'Student')), to=settings.AUTH_USER_MODEL, verbose_name='Children'),
        ),
    ]
