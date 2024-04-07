from django.db import models

class ChuniMusics(models.Model):
    title = models.CharField(max_length=255, help_text="曲名")
    genre_name = models.ForeignKey('ChuniGenres', on_delete=models.PROTECT,
                                   related_name='chuni_musics_chuni_genres', help_text="ジャンル名", null=True, blank=True)
    class Meta:
        db_table = 'chuni_musics'