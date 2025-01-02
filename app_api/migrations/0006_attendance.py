# Generated by Django 5.1.4 on 2025-01-02 03:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_api', '0005_rename_lesson_time_group_lesson_end_time_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('is_absent', models.BooleanField(default=True)),
                ('lesson', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='app_api.lesson')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='app_api.student')),
            ],
        ),
    ]