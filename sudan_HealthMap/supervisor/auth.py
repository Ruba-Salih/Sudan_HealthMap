from django.contrib.auth.backends import BaseBackend
from supervisor.models import Supervisor
from django.contrib.auth.hashers import check_password

class SupervisorBackend(BaseBackend):
    """
    Custom authentication backend for the Supervisor model.
    """

    def authenticate(self, request, username=None, password=None):
        try:
            supervisor = Supervisor.objects.get(email=username)
            if check_password(password, supervisor.password) and supervisor.is_active:
                return supervisor
        except Supervisor.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return Supervisor.objects.get(pk=user_id)
        except Supervisor.DoesNotExist:
            return None
