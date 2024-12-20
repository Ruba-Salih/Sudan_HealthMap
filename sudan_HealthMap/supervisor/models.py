from django.db import models

class Supervisor(models.Model):
    """
    Model representing a Supervisor in the system.
    
    Attributes:
        name (str): The name of the supervisor.
        email (str): The supervisor's email address, used for login.
        password (str): Hashed password for authentication purposes. 
    """
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)

    def __str__(self):
        """
        String representation of the Supervisor instance.

        Returns:
            str: The name of the supervisor.
        """
        return self.name
