# Generated by Django 4.2 on 2023-06-09 03:10

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('schoolManagement', '0002_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Result',
            new_name='SchoolResult',
        ),
    ]
