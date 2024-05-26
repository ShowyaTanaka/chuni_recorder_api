from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from chuniscore_recorder.models import (
    ChuniMusic,
    ChuniResult,
    ChuniDifficultyRank,
    ChuniUser,
)
from chuniscore_recorder.models.proxy.chuniresultex import ChuniResultEx
from chuniscore_recorder.serializers import (
    ChuniScoreRecordRegisterSerializer,
    ChuniScoreRecordListSerializer,
)
from chuniscore_recorder.utils.auth_permissions.auth import JWTTokenVerifyAuthentication


class ChuniScoreRegisterViewSet(viewsets.GenericViewSet):
    serializer_class = ChuniScoreRecordRegisterSerializer
    authentication_classes = [JWTTokenVerifyAuthentication]

    def get_queryset(self):
        return ChuniResult.objects.filter(chuni_user=self.request.user.chuni_user).all()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["max_music_id"] = ChuniMusic.objects.count()
        context["difficulty"] = ChuniDifficultyRank.objects.all()
        context["user"] = self.request.user if hasattr(self.request, "user") else None
        return context

    @action(methods=["post"], detail=False)
    def register_score(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class ChuniScoreGetViewSet(viewsets.GenericViewSet):
    serializer_class = ChuniScoreRecordListSerializer

    def get_queryset(self):
        self.queryset = ChuniResultEx.get_queryset_for_chuni_user_latest_time(
            self.kwargs["user_name"]
        )
        return super().get_queryset()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["max_music_id"] = ChuniMusic.objects.count()
        context["difficulty"] = ChuniDifficultyRank.objects.all()
        context["user"] = self.request.user if hasattr(self.request, "user") else None
        return context

    @action(methods=["get"], detail=False, url_path="get_score/(?P<user_name>\w+)")
    def get_score(self, _, user_name=None):
        if user_name is None:
            return Response({"detail": "ユーザー名が入力されていません。"}, status=400)
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return_dict = dict()
        return_dict["result"] = serializer.data
        return_dict["player_name"] = ChuniUser.objects.get(
            user_chuni_user__name=user_name
        ).player_name
        return Response(return_dict)
