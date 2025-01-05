from django.db import models
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from .models import Hospital
import logging
logger = logging.getLogger(__name__)


class HospitalToken(models.Model):
    hospital = models.OneToOneField(Hospital, on_delete=models.CASCADE)
    key = models.CharField(max_length=40, unique=True)

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        return super().save(*args, **kwargs)

    def generate_key(self):
        from rest_framework.authtoken.models import Token
        return Token().generate_key()

    def __str__(self):
        return self.key

# Custom Authentication Class
class HospitalTokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')
        logger.debug("Auth header: %s", auth_header)

        if not auth_header or not auth_header.startswith('Token '):
            logger.debug("No Authorization header or incorrect format.")
            return None

        token_key = auth_header.split('Token ')[1]
        try:
            token = HospitalToken.objects.get(key=token_key)
            logger.debug("Token valid for hospital: %s", token.hospital)
            return (token.hospital, None)
        except HospitalToken.DoesNotExist:
            logger.debug("Invalid token.")
            raise AuthenticationFailed("Invalid token")
