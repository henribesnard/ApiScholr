# Generated by Django 4.2.1 on 2023-05-23 15:12

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Establishment',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Name')),
                ('category', models.CharField(choices=[('PUBLIC', 'Public'), ('PRIVATE', 'Private')], max_length=50, verbose_name='Category')),
                ('phone_number', models.CharField(blank=True, max_length=17, null=True, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.", regex='^\\+?1?\\d{9,15}$')])),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Creation date')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Update date')),
                ('is_active', models.BooleanField(default=True, verbose_name='Active')),
            ],
            options={
                'verbose_name': 'Establishment',
                'verbose_name_plural': 'Establishments',
            },
        ),
        migrations.CreateModel(
            name='EstablishmentType',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(choices=[('PRESCHOOL', 'Preschool'), ('PRIMARY', 'Primary'), ('MIDDLE_SCHOOL', 'Middle School'), ('HIGH_SCHOOL', 'High School'), ('UNIVERSITY', 'University'), ('INSTITUTE', 'Institute'), ('TRAINING_CENTER', 'Training Center')], max_length=50, unique=True, verbose_name='Name')),
            ],
            options={
                'verbose_name': 'Establishment Type',
                'verbose_name_plural': 'Establishment Types',
            },
        ),
    ]
