# Generated by Django 4.2.1 on 2023-06-02 13:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('suivi', '0001_initial'),
        ('classes', '0002_initial'),
        ('calendrier', '0003_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='communicationbook',
            name='author',
            field=models.ForeignKey(limit_choices_to={'roles__in': ['TEACHER', 'HEAD', 'STAFF']}, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Author'),
        ),
        migrations.AddField(
            model_name='communicationbook',
            name='course',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='classes.course', verbose_name='Course'),
        ),
        migrations.AddField(
            model_name='communicationbook',
            name='photos',
            field=models.ManyToManyField(blank=True, to='suivi.photo'),
        ),
        migrations.AddField(
            model_name='communicationbook',
            name='schoolclass',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='classes.schoolclass', verbose_name='School Class'),
        ),
        migrations.AddField(
            model_name='communicationbook',
            name='student',
            field=models.ForeignKey(blank=True, limit_choices_to={'roles': 'STUDENT'}, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='communicationbook_entries', to=settings.AUTH_USER_MODEL, verbose_name='Student'),
        ),
        migrations.AddField(
            model_name='attendance',
            name='student',
            field=models.ForeignKey(limit_choices_to={'roles': 'STUDENT'}, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Student'),
        ),
        migrations.AddField(
            model_name='attendance',
            name='timeslot',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='calendrier.timeslot', verbose_name='Timeslot'),
        ),
    ]