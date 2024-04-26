from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.response import Response

from chuniscore_recorder.models import ChuniMusics, ChuniResult, ChuniDifficultyRank
from chuniscore_recorder.serializers import (
    ChuniScoreRecordRegisterSerializer,
    ChuniScoreRecordListSerializer,
)
from chuniscore_recorder.utils.auth_permissions.auth import JWTTokenVerifyAuthentication


class ChuniScoreViewSet(viewsets.GenericViewSet):
    queryset = ChuniResult.objects.all()
    serializer_class = None
    authentication_classes = [JWTTokenVerifyAuthentication]

    def get_serializer_class(self):
        # getパラメータ用にSerializerなしを返す
        if self.action == "register_score":
            return ChuniScoreRecordRegisterSerializer
        elif self.action == "get_score":
            return ChuniScoreRecordListSerializer
        return super().get_serializer_class()

    def get_queryset(self):
        if self.action == "get_score":
            return (
                ChuniResult.objects.filter(user=self.kwargs["pk"])
                .group_by("music_difficulty__music")
                .latest("play_date")
                .select_related(
                    "music_difficulty__music", "music_difficulty__difficulty_rank"
                )
            )
        return super().get_queryset()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["max_music_id"] = ChuniMusics.objects.count()
        context["difficulty"] = ChuniDifficultyRank.objects.all()
        context["user"] = self.request.user if hasattr(self.request, "user") else None
        return context

    @action(methods=["post"], detail=False)
    def register_score(self, request):
        super().create(request)

    @action(methods=["get"], detail=True)
    def get_score(self, request, pk=None):
        if pk is None:
            return Response({"detail": "ユーザー名が入力されていません。"}, status=400)
        return super().list(request)
