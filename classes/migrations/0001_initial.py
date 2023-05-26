# Generated by Django 4.2.1 on 2023-05-25 21:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('etabs', '0002_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Schoolclass',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('level', models.CharField(choices=[('MAT1', 'Maternelle 1'), ('MAT2', 'Maternelle 2'), ('C1', 'Primaire C1'), ('CP', 'Primaire CP'), ('CE1', 'Primaire CE1'), ('CE2', 'Primaire CE2'), ('CM1', 'Primaire CM1'), ('CM2', 'Primaire CM2'), ('6EME', 'Secondaire 6eme'), ('5EME', 'Secondaire 5eme'), ('4EME', 'Secondaire 4eme'), ('3EME', 'Secondaire 3eme'), ('2ND', 'Secondaire 2nd'), ('1ERE', 'Secondaire 1ere'), ('TERM', 'Secondaire Terminal'), ('L1', 'Universitaire Licence 1'), ('L2', 'Universitaire Licence 2'), ('L3', 'Universitaire Licence 3'), ('M1', 'Universitaire Master 1'), ('M2', 'Universitaire Master 2'), ('PHD', 'Doctorat')], max_length=30, verbose_name='Level')),
                ('is_active', models.BooleanField(default=True, verbose_name='Active')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Creation date')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Update date')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_classes', to=settings.AUTH_USER_MODEL, verbose_name='Created by')),
                ('establishment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='etabs.establishment', verbose_name='Establishment')),
                ('principal_teacher', models.ForeignKey(blank=True, limit_choices_to={'roles__name': 'Teacher'}, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='principal_teacher_classes', to=settings.AUTH_USER_MODEL, verbose_name='Principal teacher')),
                ('students', models.ManyToManyField(limit_choices_to={'roles__name': 'Student'}, related_name='student_classes', to=settings.AUTH_USER_MODEL, verbose_name='Students')),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='updated_classes', to=settings.AUTH_USER_MODEL, verbose_name='Updated by')),
            ],
            options={
                'verbose_name': 'Class',
                'verbose_name_plural': 'Classes',
            },
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Name')),
                ('subject', models.CharField(choices=[('MATH', 'Mathématiques'), ('PHYS', 'Physique'), ('CHIM', 'Chimie'), ('BIO', 'Biologie'), ('HIST', 'Histoire'), ('GEO', 'Géographie'), ('FR', 'Français'), ('ENG', 'Anglais'), ('PHILO', 'Philosophie'), ('ART', 'Arts'), ('MUS', 'Musique'), ('PE', 'Education Physique'), ('IT', 'Informatique'), ('ECO', 'Economie')], max_length=20, verbose_name='Subject')),
                ('coefficient', models.IntegerField(default=1, verbose_name='Coefficient')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('is_active', models.BooleanField(default=True, verbose_name='Active')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Creation date')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Update date')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_courses', to=settings.AUTH_USER_MODEL, verbose_name='Created by')),
                ('schoolclass', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='classes.schoolclass', verbose_name='Class')),
                ('teachers', models.ManyToManyField(blank=True, limit_choices_to={'roles__name': 'Teacher'}, to=settings.AUTH_USER_MODEL, verbose_name='Teachers')),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='updated_courses', to=settings.AUTH_USER_MODEL, verbose_name='Updated by')),
            ],
            options={
                'verbose_name': 'Course',
                'verbose_name_plural': 'Courses',
            },
        ),
    ]
