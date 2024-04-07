from django.db import models


class User(models.Model):
    name = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    chuni_user_name = models.CharField(max_length=255, help_text="チュウニズムのプレイヤー名")
    class Meta:
        db_table = 'users'

