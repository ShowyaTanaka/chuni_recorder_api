from django.db import models
from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.response import Response

from chuniscore_recorder.models import ChuniMusic, ChuniResult, ChuniDifficultyRank
from chuniscore_recorder.serializers import (
    ChuniScoreRecordRegisterSerializer,
    ChuniScoreRecordListSerializer,
)
from chuniscore_recorder.utils.auth_permissions.auth import JWTTokenVerifyAuthentication


class ChuniScoreRegisterViewSet(viewsets.GenericViewSet):
    queryset = ChuniResult.objects.all()
    serializer_class = ChuniScoreRecordRegisterSerializer
    authentication_classes = [JWTTokenVerifyAuthentication]

    @action(methods=["post"], detail=False)
    def register_score(self, request):
        super().create(request)


class ChuniScoreGetViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    serializer_class = ChuniScoreRecordListSerializer

    def get_queryset(self):
        results = ChuniResult.objects.all()
        result_subqs = (
            results.filter(
                chuni_user_id=self.kwargs["pk"],
                music_difficulty=models.OuterRef("music_difficulty"),
            )
            .values("music_difficulty")
            .annotate(max_time=models.Max("registered_time"))
            .values("max_time")
        )
        self.queryset = results.filter(
            chuni_user_id=self.kwargs["pk"],
            registered_time=models.Subquery(result_subqs),
        ).select_related("music_difficulty__music", "music_difficulty__difficulty_rank")
        return super().get_queryset()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["max_music_id"] = ChuniMusic.objects.count()
        context["difficulty"] = ChuniDifficultyRank.objects.all()
        context["user"] = self.request.user if hasattr(self.request, "user") else None
        return context

    @action(methods=["get"], detail=True)
    def get_score(self, request, pk=None):
        if pk is None:
            return Response({"detail": "ユーザー名が入力されていません。"}, status=400)
        return super().list(request)
