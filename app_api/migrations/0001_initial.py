# Generated by Django 5.1.4 on 2025-01-02 01:33

import app_api.managers
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('username', models.CharField(blank=True, max_length=100)),
                ('email', models.EmailField(max_length=100, unique=True)),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('profile_photo', models.ImageField(blank=True, default='users/user-default.png', upload_to='users/')),
                ('role', models.CharField(choices=[('superadmin', 'Superadmin'), ('admin', 'Admin'), ('teacher', 'Ustoz'), ('parent', 'Ota-Ona'), ('student', "O'quvchi")], default='student', max_length=10)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            managers=[
                ('objects', app_api.managers.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Admin',
            fields=[
            ],
            options={
                'verbose_name': 'Admin',
                'verbose_name_plural': 'Admins',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('app_api.user',),
        ),
        migrations.CreateModel(
            name='Parent',
            fields=[
            ],
            options={
                'verbose_name': 'Parent',
                'verbose_name_plural': 'Parents',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('app_api.user',),
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
            ],
            options={
                'verbose_name': 'Student',
                'verbose_name_plural': 'Students',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('app_api.user',),
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
            ],
            options={
                'verbose_name': 'Teacher',
                'verbose_name_plural': 'Teachers',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('app_api.user',),
        ),
        migrations.AddConstraint(
            model_name='user',
            constraint=models.UniqueConstraint(fields=('first_name', 'last_name'), name='unique_full_name'),
        ),
    ]
