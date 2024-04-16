from chuniscore_recorder.models.user import User
from django.db import transaction
from django.contrib.auth.hashers import make_password, check_password
from datetime import datetime


class UserEx(User):
    class Meta:
        proxy = True

    @classmethod
    @transaction.atomic
    def create_user(cls, name, password):
        password_hash = make_password(password)
        obj = cls.objects.create(name=name, password=password_hash)
        return obj

    @classmethod
    def get_user_permission(cls, name, password):
        if not cls.objects.filter(name=name).exists():
            return None
        user = cls.objects.get(name=name)
        if check_password(password, user.password):
            return user
        else:
            return False

    @classmethod
    def is_user_name_exist(cls, name):
        return cls.objects.filter(name=name).exists()

    @classmethod
    @transaction.atomic
    def create_refresh_token(cls, user):
        import secrets

        token = secrets.token_hex()
        user.current_refresh_token = token
        user.refresh_token_updated_at = datetime.now()
        user.save()
        return token
