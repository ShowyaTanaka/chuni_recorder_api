from rest_framework import serializers
from chuniscore_recorder.models.chuni_difficulty import ChuniDifficulty


class ChuniMusicListSerializer(serializers.ModelSerializer):
    music_title = serializers.SerializerMethodField()
    difficulty_rank = serializers.SerializerMethodField()

    class Meta:
        model = ChuniDifficulty
        fields = ("id", "music_title", "difficulty_rank", "constant")

    def get_music_title(self, obj):
        return obj.music.title

    def get_difficulty_rank(self, obj):
        return obj.difficulty_rank.difficulty_rank
