from rest_framework import generics, viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from chuniscore_recorder.serializers import TokenObtainPairSerializerForUser
from datetime import datetime, timedelta
import jwt

from config.settings import settings


class AuthUserView(APIView):
    serializer_class = TokenObtainPairSerializerForUser

    @action(methods=['post'], detail=False, url_path='login', url_name='login')
    def generate_token(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid(raise_exception=True):
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        payload = {'name': serializer.validated_data['name'],
                   'until': datetime.now() + timedelta(settings.TOKEN_LIFETIME)
                   }
        key = settings.SECRET_KEY
        token = jwt.encode(
            payload=payload,
            key=key,
            algorithm="HS256"
        )
        response = Response()
        response.set_cookie('token', token)

    @action(methods=['delete'], detail=False, url_path='logout', url_name='logout')
    def delete_token(self, request, *args, **kwargs):
        response = Response()
        response.delete_cookie('token')
        return response

    @action(methods=['get'], detail=False, url_path='check', url_name='check')
    def check_token(self, request, *args, **kwargs):
        token = request.COOKIES.get('token')
        if token is None:
            return Response({'is_authenticated': False})
        try:
            payload = jwt.decode(
                jwt=token,
                key=settings.SECRET_KEY,
                algorithms=["HS256"]
            )
        except jwt.DecodeError:
            return Response({'is_authenticated': False})
        until = datetime.fromtimestamp(payload['until'])
        if until < datetime.now():
            return Response({'is_authenticated': False})
        return Response({'is_authenticated': True})

    @action(methods=["get"], detail=False, url_path="refresh", url_name="refresh")
    def refresh_token(self, request, *args, **kwargs):
        token = request.COOKIES.get("token")
        if token is None:
            return Response({"error": "token is not found."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            payload = jwt.decode(
                jwt=token,
                key=settings.SECRET_KEY,
                algorithms=["HS256"]
            )
        except jwt.DecodeError:
            return Response({"error": "token is invalid."}, status=status.HTTP_400_BAD_REQUEST)
        until = datetime.fromtimestamp(payload['until'])
        if until < datetime.now():
            return Response({"error": "token is expired."}, status=status.HTTP_400_BAD_REQUEST)
        payload["until"] = datetime.now() + timedelta(settings.TOKEN_LIFETIME)
        token = jwt.encode(
            payload=payload,
            key=settings.SECRET_KEY,
            algorithm="HS256"
        )
        response = Response()
        response.set_cookie("token", token)
        return response

