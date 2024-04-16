from django.db import models


class ChuniUser(models.Model):
    player_name = models.CharField(max_length=255, help_text="プレイヤー名")
    best_rating = models.IntegerField(
        help_text="べ枠レーティング", null=True, blank=True
    )
    update_date = models.DateTimeField(help_text="更新日時", null=True, blank=True)

    class Meta:
        db_table = "chuni_users"
