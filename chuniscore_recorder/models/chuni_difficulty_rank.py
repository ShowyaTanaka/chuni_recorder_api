from django.db import models


class ChuniDifficultyRank(models.Model):
    difficulty_rank = models.CharField(max_length=20, help_text="難易度ランク")

    class Meta:
        db_table = "chuni_difficulty_rank"
