# Generated by Django 4.2.17 on 2025-01-03 16:26

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0006_remove_hospital_user'),
    ]

    operations = [
        #migrations.RemoveField(
            #model_name='hospital',
            #name='user',
        #),
        migrations.AddField(
            model_name='hospital',
            name='last_login',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True),
        ),
    ]
