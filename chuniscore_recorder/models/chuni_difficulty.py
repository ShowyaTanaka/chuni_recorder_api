from django.db import models


class ChuniDifficulty(models.Model):
    music = models.ForeignKey(
        "ChuniMusics",
        on_delete=models.PROTECT,
        related_name="difficulty_music",
        help_text="曲名",
    )
    difficulty_rank = models.ForeignKey(
        "ChuniDifficultyRank",
        on_delete=models.PROTECT,
        related_name="chuni_difficulty_chuni_difficulty_rank",
        help_text="難易度",
    )
    constant = models.FloatField(help_text="譜面定数")

    class Meta:
        db_table = "chuni_difficulty"
