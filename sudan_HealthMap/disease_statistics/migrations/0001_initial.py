# Generated by Django 4.2.17 on 2024-12-10 05:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('disease', '0001_initial'),
        ('hospital', '0001_initial'),
        ('case', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DiseaseStatistics',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cases', models.PositiveIntegerField()),
                ('deaths', models.PositiveIntegerField()),
                ('date_reported', models.DateField(auto_now_add=True)),
                ('case_details', models.ManyToManyField(related_name='statistics', to='case.case')),
                ('disease', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='disease.disease')),
                ('hospital', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hospital.hospital')),
            ],
        ),
    ]