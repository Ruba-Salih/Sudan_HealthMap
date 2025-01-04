from django.db import models
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from .models import Hospital

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
        if not auth_header or not auth_header.startswith('Token '):
            return None

        token_key = auth_header.split('Token ')[1]
        try:
            token = HospitalToken.objects.get(key=token_key)
            # Return the associated hospital and None (no auth backend needed for custom)
            return (token.hospital, None)
        except HospitalToken.DoesNotExist:
            raise AuthenticationFailed("Invalid token")
