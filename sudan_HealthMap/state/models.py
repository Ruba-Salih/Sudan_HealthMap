from django.db import models

class State(models.Model):
    """
    Model representing the sudan state.
    """
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        """
        String representation of the State instance.

        Returns:
            str: The name of the state.
        """
        return self.name
