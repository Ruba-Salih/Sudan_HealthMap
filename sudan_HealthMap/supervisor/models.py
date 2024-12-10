from django.db import models

class Supervisor(models.Model):
    """
    Model representing a Supervisor in the system.
    
    Attributes:
        name (str): The full name of the supervisor.
        email (str): The supervisor's unique email address, used for login and identification.
        password (str): Hashed password for authentication purposes. 
                        (Should be securely hashed before storage.)
    """
    name = models.CharField(max_length=255, help_text="Full name of the supervisor")
    email = models.EmailField(unique=True, help_text="Unique email address for the supervisor")
    password = models.CharField(max_length=128, help_text="Hashed password for the supervisor")

    def __str__(self):
        """
        String representation of the Supervisor instance.

        Returns:
            str: The name of the supervisor.
        """
        return self.name
