from django.db import models
from state.models import State
from supervisor.models import Supervisor

class Hospital(models.Model):
    """
    Model representing a Hospital in the system.

    Attributes:
        name (str): The name of the hospital.
        state (ForeignKey): The state where the hospital is located. 
                            Linked to the State model with a CASCADE delete behavior.
        supervisor (ForeignKey): The supervisor assigned to the hospital. 
                                 If the supervisor is deleted, the field is set to NULL.
        username (str): Unique username for the hospital's account, used for login.
        password (str): Hashed password for the hospital's account.
    """
    name = models.CharField(max_length=255)
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    supervisor = models.ForeignKey(Supervisor,
        on_delete=models.SET_NULL, null=True)
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128)

    def __str__(self):
        """
        String representation of the Hospital instance.

        Returns:
            str: The name of the hospital.
        """
        return self.name
