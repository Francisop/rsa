# Generated by Django 4.2 on 2023-05-13 12:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('schoolManagement', '0001_initial'),
        ('userManagement', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='school_class',
            field=models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, to='schoolManagement.schoolclass'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='school_session',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='schoolManagement.schoolsession'),
            preserve_default=False,
        ),
    ]
