from django.db import models


class ChuniResult(models.Model):
    user = models.ForeignKey(
        "ChuniUser",
        on_delete=models.CASCADE,
        related_name="result_user",
        help_text="ユーザー名",
    )
    music = models.ForeignKey(
        "ChuniMusics",
        on_delete=models.PROTECT,
        related_name="result_music",
        help_text="曲名",
    )
    difficulty = models.ForeignKey(
        "ChuniDifficulty",
        on_delete=models.PROTECT,
        related_name="result_difficulty",
        help_text="難易度",
    )
    score = models.IntegerField(help_text="スコア")
    play_date = models.DateField(help_text="プレイ日")

    class Meta:
        db_table = "chuni_result"
