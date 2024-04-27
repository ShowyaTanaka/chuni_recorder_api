from datetime import datetime, timezone

from django.db import transaction
from rest_framework import serializers
from chuniscore_recorder.models import ChuniDifficulty, ChuniResult


class ChuniScoreRecordRegisterSerializer(serializers.Serializer):

    class _ChuniScoreRecordValidationSerializer(serializers.Serializer):
        score = serializers.FloatField(
            help_text="スコア",
            required=True,
            max_value=1010000,
            min_value=0,
            error_messages={
                "required": "スコアが入力されていません",
                "max_value": "スコアが不正です",
                "min_value": "スコアが不正です",
            },
        )
        music_id = serializers.IntegerField(
            help_text="曲ID",
            required=True,
            error_messages={"required": "曲IDが入力されていません"},
        )
        difficulty = serializers.CharField(
            help_text="難易度",
            required=True,
            error_messages={"required": "難易度が入力されていません"},
        )

        def validate_music_id(self, value):
            if not value:
                raise serializers.ValidationError("曲IDが入力されていません")
            # バリデーションとしては甘いが、曲数のみから無効なIDかどうかを検証する(N+1回避)
            if value > self.context["max_music_id"] or value < 1:
                raise serializers.ValidationError("曲IDが不正です")
            return value

        def validate_difficulty(self, value):
            if (
                not self.context["difficulty"]
                .filter(chuni_difficulty_rank=value)
                .exists()
            ):
                raise serializers.ValidationError("難易度が不正です")
            return value

    score_list = serializers.ListField(
        required=True, child=_ChuniScoreRecordValidationSerializer()
    )

    def validate_score_list(self, value):
        for dict_value in value:
            serializer = self._ChuniScoreRecordValidationSerializer(
                data=dict_value, context=self.context
            )
            if not serializer.is_valid():
                error_msg = list(serializer.errors.values())[0]
                raise serializers.ValidationError(error_msg)
        return value

    @transaction.atomic
    def create(self, validated_data):
        # bulkで更新する。
        music_ids = [score["music_id"] for score in validated_data["score_list"]]
        difficulty = (
            ChuniDifficulty.objects.filter(music_id__in=music_ids)
            .select_related("difficulty_rank")
            .all()
        )
        result_list = []
        music_id_list = [score["music_id"] for score in validated_data["score_list"]]
        results = (
            ChuniResult.objects.filter(music_difficulty__music_id__in=music_id_list)
            .group_by("music_difficulty__music")
            .latest("play_time")
        )
        for score in validated_data["score_list"]:
            try:
                music_difficulty = difficulty.get(
                    music_id=score["music_id"],
                    difficulty_rank__difficulty_rank=score["difficulty"],
                )
            except ChuniDifficulty.DoesNotExist:
                # 本来バリデーション段階で弾くべきだが、クエリの発行回数を減らすためにここで弾く
                raise serializers.ValidationError(
                    "この楽曲IDには存在しない難易度が指定されています"
                )
            if results.filter(music_difficulty__music_id=score["music_id"]).exists():
                result = results.get(music_difficulty__music_id=score["music_id"])
                if result.score <= score["score"]:
                    result_list.append(
                        ChuniResult(
                            user=self.context["request"].user,
                            music_difficulty=music_difficulty,
                            score=score["score"],
                            registered_time=datetime.now(timezone.utc),
                        )
                    )
        ChuniResult.objects.bulk_create(result_list)
        return validated_data


class ChuniScoreRecordListSerializer(serializers.ModelSerializer):
    music_id = serializers.IntegerField(
        help_text="曲ID", source="music_difficulty.music_id"
    )
    difficulty = serializers.SerializerMethodField(
        help_text="難易度", method_name="get_difficulty"
    )
    music_title = serializers.SerializerMethodField(
        help_text="曲名", method_name="get_music_title"
    )
    constant = serializers.CharField(
        help_text="定数", source="music_difficulty.constant"
    )
    score = serializers.IntegerField(help_text="スコア")
    registered_time = serializers.DateTimeField(help_text="登録日")

    class Meta:
        model = ChuniResult
        fields = [
            "music_id",
            "difficulty",
            "music_title",
            "score",
            "registered_time",
            "constant",
        ]

    def get_difficulty(self, obj):
        return obj.music_difficulty.difficulty_rank.difficulty_rank

    def get_music_title(self, obj):
        return obj.music_difficulty.music.title
