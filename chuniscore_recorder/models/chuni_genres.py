from django.db import models


class ChuniGenres(models.Model):
    genre_name = models.CharField(max_length=255, help_text="ジャンル名")

    class Meta:
        db_table = "chuni_genres"
