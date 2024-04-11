from django.db import models
class ChuniUser(models.Model):
    player_name = models.CharField(max_length=255, help_text="プレイヤー名")
    best_rating = models.IntegerField(help_text="べ枠レーティング")
    update_date = models.DateTimeField(help_text="更新日時")
    class Meta:
        db_table = 'chuni_users'