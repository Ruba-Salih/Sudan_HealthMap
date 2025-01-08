from django.db import models
from disease.models import Disease
from hospital.models import Hospital

class Case(models.Model):
    """
    A model representing a single case of a disease.
    """
    status_choices = [
        ('recovered', 'Recovered'),
        ('deceased', 'Deceased'),
        ('under_treatment', 'Under Treatment'),
    ]

    season_choices = [
        ('winter', 'Winter'),
        ('spring', 'Spring'),
        ('summer', 'Summer'),
        ('autumn', 'Autumn'),
    ]

    disease = models.ForeignKey(Disease, on_delete=models.CASCADE)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    patient_number = models.IntegerField()
    patient_age = models.PositiveIntegerField()
    patient_sex = models.CharField(max_length=10)
    patient_blood_type = models.CharField(max_length=3)
    patient_status = models.CharField(max_length=20, choices=status_choices)
    main_symptom_causing_death = models.CharField(max_length=255, blank=True, null=True)
    alive = models.BooleanField(default=True)
    season = models.CharField(max_length=10, choices=season_choices)
    date_reported = models.DateField(auto_now_add=True)

    class Meta:
        """
        To make the combination of hospital and patient_number is unique.
        """
        constraints = [
            models.UniqueConstraint(fields=['hospital', 'patient_number'], name='unique_patient_number_per_hospital')
        ]

    def __str__(self):
        """
        String representation of the Case instance.
        """
        return f"Case of {self.disease.name} at {self.hospital.name} ({self.date_reported})"
