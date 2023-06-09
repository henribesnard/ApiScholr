# Generated by Django 4.2.1 on 2023-06-02 13:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('etabs', '0001_initial'),
        ('classes', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='schoolclass',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_classes', to=settings.AUTH_USER_MODEL, verbose_name='Created by'),
        ),
        migrations.AddField(
            model_name='schoolclass',
            name='establishment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='etabs.establishment', verbose_name='Establishment'),
        ),
        migrations.AddField(
            model_name='schoolclass',
            name='principal_teacher',
            field=models.ForeignKey(blank=True, limit_choices_to={'roles__name': 'Teacher'}, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='principal_teacher_classes', to=settings.AUTH_USER_MODEL, verbose_name='Principal teacher'),
        ),
        migrations.AddField(
            model_name='schoolclass',
            name='students',
            field=models.ManyToManyField(limit_choices_to={'roles__name': 'Student'}, related_name='student_classes', to=settings.AUTH_USER_MODEL, verbose_name='Students'),
        ),
        migrations.AddField(
            model_name='schoolclass',
            name='updated_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='updated_classes', to=settings.AUTH_USER_MODEL, verbose_name='Updated by'),
        ),
        migrations.AddField(
            model_name='course',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_courses', to=settings.AUTH_USER_MODEL, verbose_name='Created by'),
        ),
        migrations.AddField(
            model_name='course',
            name='schoolclass',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='classes.schoolclass', verbose_name='Class'),
        ),
        migrations.AddField(
            model_name='course',
            name='teachers',
            field=models.ManyToManyField(blank=True, limit_choices_to={'roles__name': 'Teacher'}, to=settings.AUTH_USER_MODEL, verbose_name='Teachers'),
        ),
        migrations.AddField(
            model_name='course',
            name='updated_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='updated_courses', to=settings.AUTH_USER_MODEL, verbose_name='Updated by'),
        ),
    ]
