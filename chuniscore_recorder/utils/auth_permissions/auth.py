from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions
from django.conf import settings
import jwt
from datetime import datetime
from chuniscore_recorder.models.proxy.userex import UserEx


class JWTTokenVerifyAuthentication(BaseAuthentication):
    def authenticate(self, request):
        token = request.headers.get("Token")

        if token is None:
            raise exceptions.AuthenticationFailed("Token is not found.")
        try:
            payload = jwt.decode(
                jwt=token, key=settings.SECRET_KEY, algorithms=["HS256"]
            )
        except jwt.DecodeError:
            raise exceptions.AuthenticationFailed("Invalid token.")
        if payload["until"] < datetime.now().timestamp():
            raise exceptions.AuthenticationFailed("Token is expired.")
        user = UserEx.objects.select_related("chuni_user").get(name=payload["name"])
        return user, None
