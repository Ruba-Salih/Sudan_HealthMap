# Generated by Django 4.2.17 on 2024-12-28 22:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('hospital', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='hospital',
            name='user',
            field=models.OneToOneField(default=2, limit_choices_to={'role': 'hospital'}, on_delete=django.db.models.deletion.CASCADE, related_name='hospital_account', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='hospital',
            name='supervisor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='supervised_hospitals', to=settings.AUTH_USER_MODEL),
        ),
    ]