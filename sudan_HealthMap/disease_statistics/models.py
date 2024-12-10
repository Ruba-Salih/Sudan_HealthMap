from django.db import models
from disease.models import Disease
from hospital.models import Hospital
from case.models import Case

class DiseaseStatistics(models.Model):
    """
    A model representing disease statistics for a specific disease.

    Attributes:
        hospital (ForeignKey): The hospital where the statistics were recorded.
        disease (ForeignKey): The disease to which the statistics relate.
        cases (PositiveIntegerField): The total number of cases reported.
        deaths (PositiveIntegerField): The total number of deaths recorded.
        date_reported (DateField): The date when these statistics were recorded.
        case_details (ManyToManyField): A field linking to individual Case records.
    """
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    disease = models.ForeignKey(Disease, on_delete=models.CASCADE)
    cases = models.PositiveIntegerField()
    deaths = models.PositiveIntegerField()
    date_reported = models.DateField(auto_now_add=True)
    case_details = models.ManyToManyField(Case, related_name='statistics')

    def __str__(self):
        """
        String representation of the DiseaseStatistics instance.

        Returns:
            str: A summary that includ the disease name, hospital name, and date of the report.
        """
        return f"Disease statistics for {self.disease.name} at {self.hospital.name} ({self.date_reported})"
