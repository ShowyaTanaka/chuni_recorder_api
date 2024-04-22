from django_filters import rest_framework as filters

from chuniscore_recorder.models import ChuniDifficultyRank
from chuniscore_recorder.models.chuni_difficulty import ChuniDifficulty


class ChuniMusicFilter(filters.FilterSet):
    contain_worlds_end = filters.BooleanFilter(method="contain_we_filter")
    contain_ultima = filters.BooleanFilter(method="contain_ult_filter")

    def contain_we_filter(self, queryset, name, value):
        """
        :param queryset: chuniscore_recorder.models.chuni_difficulty.objects.all()
        :param name:
        :param value:
        :return:
        """
        difficulty_rank = ChuniDifficultyRank.objects.get(difficulty_rank="WORLD'S END")
        if value:
            return queryset.filter(difficulty_music__difficulty_rank=difficulty_rank)
        return queryset

    def contain_ult_filter(self, queryset, name, value):
        """
        :param queryset: chuniscore_recorder.models.chuni_difficulty.objects.all()
        :param name:
        :param value:
        :return:
        """
        difficulty_rank = ChuniDifficultyRank.objects.get(difficulty_rank="ULTIMA")
        if value:
            return queryset.filter(difficulty_music__difficulty_rank=difficulty_rank)
        return queryset
