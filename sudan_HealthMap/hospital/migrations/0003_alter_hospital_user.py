# Generated by Django 4.2.17 on 2024-12-29 02:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('hospital', '0002_hospital_user_alter_hospital_supervisor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hospital',
            name='user',
            field=models.ForeignKey(limit_choices_to={'role': 'hospital'}, on_delete=django.db.models.deletion.CASCADE, related_name='hospitals', to=settings.AUTH_USER_MODEL),
        ),
    ]
