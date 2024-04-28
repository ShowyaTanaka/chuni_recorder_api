from django.db.models import OuterRef, Subquery, Max
from django.db import transaction
from chuniscore_recorder.models import ChuniResult


class ChuniResultEx(ChuniResult):
    class Meta:
        proxy = True

    @classmethod
    @transaction.atomic
    def get_queryset_for_chuni_user_latest_time(cls, chuni_user_id: str):
        results = ChuniResult.objects.all()
        result_subqs = (
            results.filter(
                chuni_user_id=chuni_user_id,
                music_difficulty=OuterRef("music_difficulty"),
            )
            .values("music_difficulty")
            .annotate(max_time=Max("registered_time"))
            .values("max_time")
        )
        queryset = results.filter(
            chuni_user_id=chuni_user_id,
            registered_time=Subquery(result_subqs),
        ).select_related("music_difficulty__music", "music_difficulty__difficulty_rank")
        return queryset
