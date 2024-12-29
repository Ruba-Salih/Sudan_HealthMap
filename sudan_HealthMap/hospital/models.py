from django.db import models
from django.conf import settings
from state.models import State
from supervisor.models import Supervisor

class Hospital(models.Model):
    """
    Model representing a Hospital in the system.

    Attributes:
        name (str): The name of the hospital.
        state (ForeignKey): The state where the hospital is located. 
        supervisor (ForeignKey): The supervisor assigned to the hospital. 
        username (str): Username for the hospital's account, used for login.
        password (str): Password for the hospital's account.
    """

    user = models.ForeignKey(Supervisor,
                                on_delete=models.CASCADE,
                                related_name='hospitals',
                                limit_choices_to={'role': 'hospital'})
    name = models.CharField(max_length=255)
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    supervisor = models.ForeignKey(Supervisor,
                                   on_delete=models.SET_NULL, null=True,
                                   related_name='supervised_hospitals')
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128)

    def __str__(self):
        """
        String representation of the Hospital instance.

        Returns:
            str: The name of the hospital.
        """
        return self.name
