from django.db import models
from disease.models import Disease
from hospital.models import Hospital

class Case(models.Model):
    """
    A model representing a single case of a disease.

    Attributes:
        status_choices (list): Predefined choices for the status.
        season_choices (list): Predefined choices for the season.
        disease (ForeignKey): The disease related to this case.
        hospital (ForeignKey): The hospital where the case was reported.
        patient_age (PositiveIntegerField): The age of the patient.
        patient_sex (CharField): The sex of the patient.
        patient_blood_type (CharField): The blood type of the patient.
        patient_status (CharField): The status of the case.
        main_symptom_causing_death (CharField): The main symptoms causing death, if applicable.
        alive (BooleanField): Indicates whether the patient is alive or deceased.
        season (CharField): The season during which the case was reported.
        date_reported (DateField): The date the case was reported.

    Methods:
        __str__(): Returns a string representation of the case, including the disease name, hospital name, and date reported.
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
    patient_age = models.PositiveIntegerField()
    patient_sex = models.CharField(max_length=10)
    patient_blood_type = models.CharField(max_length=3)
    patient_status = models.CharField(max_length=20, choices=status_choices)
    main_symptom_causing_death = models.CharField(max_length=255, blank=True, null=True)
    alive = models.BooleanField(default=True)
    season = models.CharField(max_length=10, choices=season_choices)
    date_reported = models.DateField(auto_now_add=True)

    def __str__(self):
        """
        String representation of the Case instance.

        Returns:
            str: A string representation of the case including the disease name, hospital name, and the date reported.
        """
        return f"Case of {self.disease.name} at {self.hospital.name} ({self.date_reported})"
