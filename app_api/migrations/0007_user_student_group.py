# Generated by Django 5.1.4 on 2025-01-03 01:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_api', '0006_attendance'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='student_group',
            field=models.ManyToManyField(to='app_api.group'),
        ),
    ]