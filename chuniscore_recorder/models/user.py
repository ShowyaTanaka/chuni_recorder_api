from django.db import models


class User(models.Model):
    name = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    chuni_user = models.OneToOneField('ChuniUser', on_delete=models.CASCADE, related_name='user_chuni_user', help_text="チュウニズムのプレイヤー名", null=True, blank=True)


    class Meta:
        db_table = 'users'

