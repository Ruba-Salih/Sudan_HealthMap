from django.conf import settings
from django.db import models

class Disease(models.Model):
    """
    Model representing a disease in the system.

    Attributes:
        name (str): The name of the disease.
        description (str): A detailed description of the disease.
    """
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
                                   null=True, blank=True)

    def __str__(self):
        """
        String representation of the Disease instance.

        Returns:
            str: The name of the disease.
        """
        return self.name
