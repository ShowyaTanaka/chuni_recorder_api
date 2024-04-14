from rest_framework import serializers
from chuniscore_recorder.models import ChuniMusics

class ChuniScoreRecordRegisterSerializer(serializers.Serializer):

    score = serializers.FloatField(help_text="スコア", required=True, max_value=1010000, min_value=0)
    music_id = serializers.IntegerField(help_text="曲ID", required=True)
    difficulty = serializers.CharField(help_text="難易度", required=True)

    def validate_music_id(self, value):
        if not value:
            raise serializers.ValidationError("曲IDが入力されていません")
        # バリデーションとしては甘いが、曲数のみから無効なIDかどうかを検証する(N+1回避)
