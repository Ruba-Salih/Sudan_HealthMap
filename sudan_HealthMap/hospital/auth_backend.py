from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.hashers import check_password
from hospital.models import Hospital

class HospitalBackend(BaseBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        try:
            hospital = Hospital.objects.get(email=email)
            if check_password(password, hospital.password):
                return hospital
        except Hospital.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            hospital = Hospital.objects.get(pk=user_id)
            setattr(hospital, 'is_active', True)
            return hospital
        except Hospital.DoesNotExist:
            return None
