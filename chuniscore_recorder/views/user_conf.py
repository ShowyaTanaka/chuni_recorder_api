from rest_framework.decorators import action
from rest_framework.response import Response

from chuniscore_recorder.models.proxy.userex import UserEx
from rest_framework import viewsets, status
from chuniscore_recorder.serializers.user_conf import CreateUserSerializer
from chuniscore_recorder.utils.auth_util import AuthUtilEx

class UserConfigCreateViewSet(viewsets.GenericViewSet, viewsets.mixins.CreateModelMixin):
    serializer_class = CreateUserSerializer


