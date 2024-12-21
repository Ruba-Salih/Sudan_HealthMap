# Generated by Django 4.2.17 on 2024-12-10 05:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('state', '0001_initial'),
        ('supervisor', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Hospital',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('username', models.CharField(max_length=150, unique=True)),
                ('password', models.CharField(max_length=128)),
                ('state', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='state.state')),
                ('supervisor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='supervisor.supervisor')),
            ],
        ),
    ]