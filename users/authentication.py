from rest_framework_simplejwt.authentication import JWTAuthentication
from django.utils.timezone import now

class CustomJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        response = super().authenticate(request)
        if response is not None:
            user, token = response
            user.last_login = now()
            user.save(update_fields=['last_login'])
        return response