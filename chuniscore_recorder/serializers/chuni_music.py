from rest_framework import serializers
from chuniscore_recorder.models.chuni_difficulty import ChuniDifficulty


class ChuniMusicListSerializer(serializers.ModelSerializer):
    music_title = serializers.SerializerMethodField()

    class Meta:
        model = ChuniDifficulty
        fields = ("id", "music_title")

    def get_music_title(self, obj):
        return obj.title
