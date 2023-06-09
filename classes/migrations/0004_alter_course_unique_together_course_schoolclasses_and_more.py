# Generated by Django 4.2.1 on 2023-06-29 19:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classes', '0003_alter_course_unique_together_and_more'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='course',
            unique_together=set(),
        ),
        migrations.AddField(
            model_name='course',
            name='schoolclasses',
            field=models.ManyToManyField(to='classes.schoolclass', verbose_name='Classes'),
        ),
        migrations.RemoveField(
            model_name='course',
            name='schoolclass',
        ),
    ]
