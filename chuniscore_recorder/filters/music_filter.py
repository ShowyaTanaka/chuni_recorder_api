from django_filters import rest_framework as filters
from chuniscore_recorder.models.chuni_difficulty import ChuniDifficulty

class ChuniMusicFilter(filters.FilterSet):
    contain_worlds_end = filters.BooleanFilter(method='contain_we_filter')
    contain_ultima = filters.BooleanFilter(method='contain_ult_filter')
    difficulty = filters.CharFilter(method='difficulty_filter')

    def contain_we_filter(self, queryset, name , value):
        """
        :param queryset: chuniscore_recorder.models.chuni_difficulty.objects.all()
        :param name:
        :param value:
        :return:
        """
        if value:
            return queryset.filter(difficulty_rank__difficulty_rank='WORLD\'S END')
        return queryset

    def contain_ult_filter(self, queryset,name, value):
        """
        :param queryset: chuniscore_recorder.models.chuni_difficulty.objects.all()
        :param name:
        :param value:
        :return:
        """
        if value:
            return queryset.filter(difficulty_rank__difficulty_rank='ULTIMA')
        return queryset

    def difficulty_filter(self, queryset, name, value):
        if value=='bas':
            return queryset.filter(difficulty_rank__difficulty_rank='BASIC')
        elif value=='adv':
            return queryset.filter(difficulty_rank__difficulty_rank='ADVANCED')
        elif value=='exp':
            return queryset.filter(difficulty_rank__difficulty_rank='EXPERT')
        elif value=='mas':
            return queryset.filter(difficulty_rank__difficulty_rank='MASTER')
        elif value=='ult':
            return queryset.filter(difficulty_rank__difficulty_rank='ULTIMA')
        elif value=='we':
            return queryset.filter(difficulty_rank__difficulty_rank='WORLD\'S END')