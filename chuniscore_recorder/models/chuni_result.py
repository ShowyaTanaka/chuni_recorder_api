from django.db import models


class ChuniResult(models.Model):
    chuni_user = models.ForeignKey(
        "ChuniUser",
        on_delete=models.CASCADE,
        related_name="result_user",
        help_text="ユーザー名",
    )
    music_difficulty = models.ForeignKey(
        "ChuniDifficulty",
        on_delete=models.PROTECT,
        related_name="result_music",
        help_text="曲名",
    )
    score = models.IntegerField(help_text="スコア")
    registered_time = models.DateTimeField(help_text="登録日")

    class Meta:
        db_table = "chuni_result"
