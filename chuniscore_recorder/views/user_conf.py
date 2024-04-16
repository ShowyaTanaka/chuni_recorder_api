from rest_framework import viewsets
from chuniscore_recorder.serializers import (
    CreateUserSerializer,
    UpdateChuniUserSerializer,
)
from chuniscore_recorder.utils.auth_permissions.auth import JWTTokenVerifyAuthentication
from rest_framework.decorators import action


class UserConfigCreateViewSet(
    viewsets.GenericViewSet, viewsets.mixins.CreateModelMixin
):
    serializer_class = CreateUserSerializer


class UserConfigModifyViewSet(
    viewsets.GenericViewSet, viewsets.mixins.UpdateModelMixin
):
    authentication_classes = [JWTTokenVerifyAuthentication]

    def get_serializer_class(self):
        if self.action == "update_chuni_player_name":
            return UpdateChuniUserSerializer
        return super().get_serializer_class()

    @action(methods=["patch"], detail=False)
    def update_chuni_player_name(self, request):
        super().update(request)
