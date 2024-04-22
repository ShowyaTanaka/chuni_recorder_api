from chuniscore_recorder.models import User, ChuniUser
from django.db import transaction
from chuniscore_recorder.models import ChuniResult


class ChuniResultEx(ChuniResult):
    class Meta:
        proxy = True

    @classmethod
    @transaction.atomic
    def fetch_user_result(cls, user: User):
        return cls.objects.filter(user=user).group_by("music_difficulty__music").latest("play_time")
