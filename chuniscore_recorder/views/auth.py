from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView

from chuniscore_recorder.models.proxy import UserEx
from chuniscore_recorder.serializers import TokenObtainPairSerializerForUser
from datetime import datetime, timezone
import jwt
from chuniscore_recorder.utils.auth_util import AuthUtilEx
from chuniscore_recorder.utils.auth_permissions.auth import JWTTokenVerifyAuthentication
from config import settings


class AuthUserLoginView(viewsets.GenericViewSet):
    @action(methods=["post"], detail=False)
    def create_user(self, request, *args, **kwargs):
        serializer = TokenObtainPairSerializerForUser(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        response = Response(serializer.data)
        token = UserEx.create_refresh_token(user)
        response.set_cookie(
            "refresh_token", token, httponly=True, max_age=60 * 60 * 24 * 14
        )
        return response

    @action(methods=["post"], detail=False, url_path="login", url_name="login")
    def login(self, request, *args, **kwargs):
        serializer = TokenObtainPairSerializerForUser(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        user = UserEx.get_user_permission(
            serializer.validated_data["user_name"],
            serializer.validated_data["password"],
        )
        if not user:
            return Response(
                {"error": "User authentication failed."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        token = AuthUtilEx.create_token(user.name)
        refresh_token = UserEx.create_refresh_token(user)
        response = Response({"token": token, "user_name": user.name, "contain_chuni_user": user.chuni_user is not None})
        response.set_cookie(
            "refresh_token", refresh_token, httponly=True, max_age=60 * 60 * 24 * 14
        )
        return response


class AuthUserCheckView(APIView):

    serializer_class = None

    def get(self, request, *args, **kwargs):
        token = request.headers.get("Token")
        if token is None:
            return Response({"is_authenticated": False})
        try:
            payload = jwt.decode(
                jwt=str(token), key=settings.SECRET_KEY, algorithms=["HS256"]
            )
        except jwt.DecodeError:
            return Response({"is_authenticated": False})
        until = datetime.fromtimestamp(payload["until"])
        if until < datetime.now():
            return Response({"is_authenticated": False})
        return Response({"is_authenticated": True})


class AuthUserJWTOperateView(viewsets.GenericViewSet):
    authentication_classes = [JWTTokenVerifyAuthentication]

    @action(methods=["delete"], detail=False, url_path="logout", url_name="logout")
    def delete_token(self, request, *args, **kwargs):
        if request.user.current_refresh_token != request.COOKIES.get("refresh_token"):
            return Response(
                {"detail": "Refresh token is invalid."},
                status=status.HTTP_403_FORBIDDEN,
            )
        request.user.current_refresh_token = None
        request.user.refresh_token_updated_at = None
        request.user.save()
        response = Response()
        response.delete_cookie("refresh_token")
        return response

    @action(methods=["get"], detail=False)
    def my_status(self, request, *args, **kwargs):
        print(self.request.user.player_name)
        return Response(
            {
                "user_name": self.request.user.name,
                "chuni_player_name": (
                    self.request.user.chuni_user.player_name
                    if self.request.user.chuni_user is not None
                    else None
                ),
                "chuni_user_id": (
                    self.request.user.chuni_user.id
                    if self.request.user.chuni_user is not None
                    else None
                ),
            }
        )


class AuthUserJWTRefreshView(viewsets.GenericViewSet):
    @action(methods=["get"], detail=False, url_path="refresh", url_name="refresh")
    def refresh_token(self, request, *args, **kwargs):
        # DjangoのSerializerでは、cookieの処理が非常にやりにくいため、ベタ書きする。
        token = request.COOKIES.get("refresh_token")
        if token is None:
            return Response(
                {"detail": "Refresh token is not found."},
                status=status.HTTP_403_FORBIDDEN,
            )
        # nameにUNIQUE制約がかかっているため,firstで検索しても問題ない。
        user = UserEx.objects.filter(
            name=request.headers.get("user_name"), current_refresh_token=token
        ).first()
        if user is None:
            return Response(
                {"detail": "Token is invalid."}, status=status.HTTP_403_FORBIDDEN
            )
        print(user.refresh_token_updated_at + settings.REFRESH_TOKEN_LIFETIME)
        if (
            user.refresh_token_updated_at + settings.REFRESH_TOKEN_LIFETIME
            < datetime.now(timezone.utc)
        ):
            return Response(
                {"detail": "Token is expired."}, status=status.HTTP_403_FORBIDDEN
            )
        refresh_token = UserEx.create_refresh_token(user=user)
        token = AuthUtilEx.create_token(user.name)
        response = Response({"token": token})
        response.set_cookie(
            "refresh_token", refresh_token, httponly=True, max_age=60 * 60 * 24 * 14
        )
        return response
