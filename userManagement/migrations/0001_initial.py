# Generated by Django 4.2 on 2023-06-10 13:04

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('schoolManagement', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(blank=True, max_length=20, null=True, unique=True, verbose_name='username')),
                ('first_name', models.CharField(max_length=150)),
                ('last_name', models.CharField(max_length=150)),
                ('other_name', models.CharField(blank=True, max_length=150, null=True)),
                ('role', models.CharField(choices=[('admin', 'admin'), ('student', 'student')], default='admin', max_length=150)),
                ('gender', models.CharField(choices=[('male', 'm'), ('female', 'f')], max_length=150)),
                ('matric', models.CharField(blank=True, max_length=150, null=True, unique=True)),
                ('session_name', models.CharField(max_length=150)),
                ('class_name', models.CharField(max_length=150)),
                ('start_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('school_class', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='schoolManagement.schoolclass')),
                ('session', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='schoolManagement.schoolsession')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
