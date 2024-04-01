from django.db import models
from django.contrib.auth.hashers import make_password, check_password
import hashlib

class User(models.Model):
    name = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = 'users'

    @classmethod
    def create_user(cls, name, password):
        password_hash = make_password(password)
        cls.objects.create(name=name, password=password_hash)

    @classmethod
    def get_user_permission(cls, name, password):
        if not cls.objects.filter(name=name).exists():
            return None
        user = cls.objects.get(name=name)
        if check_password(password, user.password):
            return user
        else:
            return False