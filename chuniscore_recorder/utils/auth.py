from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions
from django.conf import settings
import jwt
from datetime import datetime


class JWTTokenVerifyAuthentication(BaseAuthentication):
    def authenticate(self, request):
        token = request.COOKIES.get('token')
        if token is None:
            return None
        try:
            payload = jwt.decode(
                jwt=token,
                key=settings.SECRET_KEY,
                algorithms=["HS256"]
            )
        except jwt.DecodeError:
            raise exceptions.AuthenticationFailed('Invalid token.')
        if payload['until'] < datetime.now().timestamp():
            raise exceptions.AuthenticationFailed('Token is expired.')
        return (payload, None)
