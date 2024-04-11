from rest_framework import viewsets, mixins
from chuniscore_recorder.models.chuni_difficulty import ChuniDifficulty
from chuniscore_recorder.serializers.chuni_music import ChuniMusicListSerializer
from chuniscore_recorder.filters.music_filter import ChuniMusicFilter
from django_filters.rest_framework import DjangoFilterBackend

class ChuniMusicViewSet(viewsets.ModelViewSet, mixins.ListModelMixin):
    queryset = ChuniDifficulty.objects.all().select_related('music', 'difficulty_rank')
    filter_backends = [DjangoFilterBackend]
    serializer_class = ChuniMusicListSerializer
    filter_class = ChuniMusicFilter
    filterset_class = ChuniMusicFilter
    pagination_class = None
