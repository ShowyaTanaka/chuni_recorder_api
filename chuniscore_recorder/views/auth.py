from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView

from chuniscore_recorder.serializers import TokenObtainPairSerializerForUser
from datetime import datetime
import jwt
from chuniscore_recorder.utils.auth_util import AuthUtilEx
from chuniscore_recorder.utils.auth_permissions.auth import JWTTokenVerifyAuthentication
from config import settings


class AuthUserLoginView(viewsets.GenericViewSet, viewsets.mixins.CreateModelMixin):

    serializer_class = TokenObtainPairSerializerForUser



class AuthUserCheckView(APIView):

    serializer_class = None

    def get(self, request, *args, **kwargs):
        token = request.headers.get('Token')
        if token is None:
            return Response({'is_authenticated': False})
        try:
            payload = jwt.decode(
                jwt=str(token),
                key=settings.SECRET_KEY,
                algorithms=["HS256"]
            )
        except jwt.DecodeError:
            return Response({'is_authenticated': False})
        until = datetime.fromtimestamp(payload['until'])
        if until < datetime.now():
            return Response({'is_authenticated': False})
        return Response({'is_authenticated': True})


class AuthUserJWTOperateView(viewsets.GenericViewSet):
    authentication_classes = [JWTTokenVerifyAuthentication]
    serializer_class = None

    @action(methods=['delete'], detail=False, url_path='logout', url_name='logout')
    def delete_token(self, request, *args, **kwargs):
        response = Response()
        response.delete_cookie('token')
        return response


    @action(methods=["get"], detail=False, url_path="refresh", url_name="refresh")
    def refresh_token(self, request, *args, **kwargs):
        token = request.headers.get("Token")
        if token is None:
            return Response({"error": "token is not found."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            payload = jwt.decode(
                token,
                key=settings.SECRET_KEY,
                algorithms=["HS256"]
            )
        except jwt.DecodeError:
            return Response({"error": "token is invalid."}, status=status.HTTP_400_BAD_REQUEST)
        until = datetime.fromtimestamp(payload['until'])
        if until < datetime.now():
            return Response({"error": "token is expired."}, status=status.HTTP_400_BAD_REQUEST)
        token = AuthUtilEx.create_token(payload['name'])
        response = Response({"token": token})
        return response