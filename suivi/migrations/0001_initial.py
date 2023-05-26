# Generated by Django 4.2.1 on 2023-05-26 08:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('classes', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('calendrier', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('image', models.ImageField(upload_to='communicationbook_photos/')),
            ],
            options={
                'verbose_name': 'Photo',
                'verbose_name_plural': 'Photos',
            },
        ),
        migrations.CreateModel(
            name='CommunicationBook',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('message', models.TextField(verbose_name='Message')),
                ('homework', models.TextField(blank=True, null=True, verbose_name='Homework')),
                ('parent_seen', models.BooleanField(default=False, verbose_name='Parent has seen')),
                ('parent_acknowledged', models.BooleanField(default=False, verbose_name='Parent has acknowledged')),
                ('author', models.ForeignKey(limit_choices_to={'roles__in': ['TEACHER', 'HEAD', 'STAFF']}, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Author')),
                ('course', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='classes.course', verbose_name='Course')),
                ('photos', models.ManyToManyField(blank=True, to='suivi.photo')),
                ('schoolclass', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='classes.schoolclass', verbose_name='School Class')),
                ('student', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='communicationbook_entries', to=settings.AUTH_USER_MODEL, verbose_name='Student')),
            ],
            options={
                'verbose_name': 'Communication Book',
                'verbose_name_plural': 'Communication Books',
            },
        ),
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('status', models.CharField(choices=[('PRESENT', 'Present'), ('ABSENT', 'Absent'), ('LATE', 'Late'), ('EXCUSED', 'Excused')], default='PRESENT', max_length=10, verbose_name='Status')),
                ('remarks', models.TextField(blank=True, null=True, verbose_name='Remarks')),
                ('student', models.ForeignKey(limit_choices_to={'roles': 'STUDENT'}, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Student')),
                ('timeslot', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='calendrier.timeslot', verbose_name='Timeslot')),
            ],
            options={
                'verbose_name': 'Attendance',
                'verbose_name_plural': 'Attendances',
            },
        ),
    ]
