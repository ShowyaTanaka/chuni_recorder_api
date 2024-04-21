from chuniscore_recorder.models import User, ChuniUser
from django.db import transaction
from chuniscore_recorder.models import ChuniResult


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
