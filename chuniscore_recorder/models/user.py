from django.db import models


class User(models.Model):
    name = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    chuni_user = models.OneToOneField(
        "ChuniUser",
        on_delete=models.CASCADE,
        related_name="user_chuni_user",
        help_text="チュウニズムのプレイヤー名",
        null=True,
        blank=True,
    )
    current_refresh_token = models.CharField(max_length=255, null=True, blank=True)
    refresh_token_updated_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "users"
