from chuniscore_recorder.models import User, ChuniUser
from django.db import transaction
from chuniscore_recorder.models import ChuniResult
from django.db.models import F, Sum, Count, Case, When, Value, FloatField, Avg


class ChuniUserEx(ChuniUser):

    class Meta:
        proxy = True

    @classmethod
    @transaction.atomic
    def create_chuni_user(cls, user: User, name: str):
        # チュウニズムのユーザー作成を行う。
        # すべてのchuniuserはuserと連携しているため,ここにユニーク制約を設けることはない。
        if user.chuni_user is not None:
            raise ValueError("User already has chuni_user.")
        obj = cls.objects.create(player_name=name, best_rating=0, update_date=None)
        user.chuni_user = obj
        user.save()
        return user

    @classmethod
    @transaction.atomic
    def delete_chuni_user(cls, user: User):
        if user.chuni_user is None:
            raise ValueError("User does not have chuni_user.")
        user.chuni_user.delete()
        user.save()
        return True

    @classmethod
    @transaction.atomic
    def reset_chuni_user_record(cls, user: User):
        # ここの機能については考慮の余地ありなので関数は実装しておくが利用しない。
        if user.chuni_user is None:
            raise ValueError("User does not have chuni_user.")
        user.chuni_user.rating = 0
        user.chuni_user.save()
        ChuniResult.objects.filter(chuni_user=user.chuni_user).delete()
        return user.chuni_user

    @classmethod
    @transaction.atomic
    def update_chuni_player_name(cls, user: User, name: str):
        if user.chuni_user is None:
            raise ValueError("User does not have chuni_user.")
        user.chuni_user.player_name = name
        user.chuni_user.save()
        return user.chuni_user

    @classmethod
    @transaction.atomic
    def refresh_chuni_rating(cls, user: User):
        if user.chuni_user is None:
            raise ValueError("User does not have chuni_user.")
        # 単曲レートはレート値計算式の変化、および譜面定数の変化といったものに大きく影響を受けるので、データとしては保管せずレート値を計算して取得する。
        # 注意点:クエリの重さが現状評価できていないため、実際に利用しながら様子を見る必要がある。(スコア登録時だけなら最悪まぁ...)
        best_ratings = (
            ChuniResult.objects.filter(chuni_user=user.chuni_user)
            .group_by("music_difficulty__music")
            .latest("play_date")
            .annotate(
                rating=Case(
                    When(
                        score__gte=1009000,
                        then=Value(F("music_difficulty__constant") + 2.15),
                    ),
                    When(
                        score__gte=1007500,
                        then=Value(
                            F("music_difficulty_constant")
                            + 2.0
                            + (F("score") - 1007500) / 10000
                        ),
                    ),
                    When(
                        score__gte=1005000,
                        then=Value(
                            F("music_difficulty__constant")
                            + 1.5
                            + (F("score") - 1005000) / 5000
                        ),
                    ),
                    When(
                        score__gte=1000000,
                        then=Value(
                            F("music_difficulty__constant")
                            + 1.0
                            + (F("score") - 1007500) / 10000
                        ),
                    ),
                    When(
                        score__gte=975000,
                        then=Value(
                            F("music_difficulty__constant")
                            + (F("score") - 975000) / 25000
                        ),
                    ),
                    When(
                        score__gte=925000,
                        then=Value(F("music_difficulty__constant") - 3.0),
                    ),
                    When(
                        score__gte=900000,
                        then=Value(F("music_difficulty__constant") - 5.0),
                    ),
                    When(
                        score__gte=800000,
                        then=Value((F("music_difficulty__constant") - 5.0) / 2),
                    ),
                    default=0,
                    output_field=FloatField(),
                )
            )
            .order_by("rating")[:30]
        )
        avg_rating = best_ratings.aggregate(Avg("rating"))["rating__avg"]
        user.chuni_user.best_rating = avg_rating
        return user.chuni_user