# Generated by Django 4.2.1 on 2023-07-18 16:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('classes', '0004_alter_course_unique_together_course_schoolclasses_and_more'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='course',
            unique_together={('name', 'subject')},
        ),
    ]