from rest_framework import viewsets, status
from rest_framework.response import Response

from chuniscore_recorder.serializers import (
    CreateUserSerializer,
    UpdateChuniUserSerializer,
    CreateChuniUserSerializer,
)
from chuniscore_recorder.utils.auth_permissions.auth import JWTTokenVerifyAuthentication
from rest_framework.decorators import action


class UserConfigCreateViewSet(
    viewsets.GenericViewSet, viewsets.mixins.CreateModelMixin
):
    serializer_class = CreateUserSerializer


class UserConfigModifyViewSet(viewsets.GenericViewSet):
    authentication_classes = [JWTTokenVerifyAuthentication]

    def get_serializer_class(self):
        if self.action == "new_chuni_user":
            return CreateChuniUserSerializer
        return super().get_serializer_class()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["user"] = self.request.user
        return context

    @action(methods=["post"], detail=False)
    def new_chuni_user(self, request):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(serializer.data, status=200)

    @action(methods=["patch"], detail=False)
    def chuni_player_name(self, request):
        user = self.request.user
        serializer = UpdateChuniUserSerializer(
            data=request.data, context={"user": user}
        )
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.update(user, serializer.validated_data)
        return Response(serializer.data, status=200)
