from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from .hospital_service import create_hospital_account

class SupervisorManager(BaseUserManager):
    def create_user(self, email, name, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set.")
        email = self.normalize_email(email)
        supervisor = self.model(email=email, name=name, **extra_fields)
        supervisor.set_password(password)
        supervisor.save(using=self._db)
        return supervisor

    def create_superuser(self, email, name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, name, password, **extra_fields)


class Supervisor(AbstractBaseUser, PermissionsMixin):
    """
    Custom Supervisor model that extends AbstractBaseUser and PermissionsMixin.
    """
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    groups = models.ManyToManyField(
        "auth.Group",
        related_name="supervisor_set",  # Avoid conflict with default user model
        blank=True,
        help_text="The groups this user belongs to.",
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="supervisor_set",  # Avoid conflict with default user model
        blank=True,
        help_text="Specific permissions for this user.",
    )

    objects = SupervisorManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.email

    def create_hospital_account(self, name, state, username, password):
        return create_hospital_account(self, name, state, username, password)
