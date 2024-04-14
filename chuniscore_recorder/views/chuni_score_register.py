from rest_framework import viewsets, mixins
from rest_framework.decorators import action

from chuniscore_recorder.models import ChuniMusics, ChuniResult
from chuniscore_recorder.serializers import ChuniScoreRecordRegisterSerializer
from chuniscore_recorder.utils.auth_permissions.auth import JWTTokenVerifyAuthentication


class ChuniScoreViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin):
    queryset = ChuniResult.objects.all()
    serializer_class = ChuniScoreRecordRegisterSerializer
    authentication_classes = [JWTTokenVerifyAuthentication]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["max_music_id"] = ChuniMusics.objects.count()
        return context

    @action(methods=['post'], detail=False)
    def register_score(self, request):
        super().create(request)

