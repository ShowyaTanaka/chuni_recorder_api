from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from rest_framework import serializers
from rest_framework.response import Response

from chuniscore_recorder.models.proxy.userex import UserEx
from chuniscore_recorder.utils.auth_util import AuthUtilEx
from chuniscore_recorder.models.proxy.chuniuserex import ChuniUserEx


class CreateUserSerializer(serializers.Serializer):

    user_name = serializers.CharField(max_length=20, write_only=True, required=True)
    password = serializers.CharField(write_only=True, required=True)

    def validate_user_name(self, value):
        if len(value) != len(value.encode("utf-8")):
            raise serializers.ValidationError(
                "ユーザー名に用いる文字列はすべて半角である必要があります。"
            )
        if UserEx.is_user_name_exist(value):
            raise serializers.ValidationError(
                "既に存在するユーザー名です。ほかのユーザー名を利用してください。"
            )
        return value

    def validate_password(self, value):
        try:
            validate_password(value)
        except ValidationError as e:
            raise serializers.ValidationError(e)
        if len(value) != len(value.encode("utf-8")):
            raise serializers.ValidationError(
                "パスワードに用いる文字列はすべて半角である必要があります。"
            )
        return value

    def to_representation(self, instance):
        token = AuthUtilEx.create_token(instance.name)
        return {"token": token.decode(), "contain_chuni_user": False}

    def create(self, validated_data):
        user = UserEx.create_user(
            validated_data["user_name"], validated_data["password"]
        )
        return user


class UpdateChuniUserSerializer(serializers.Serializer):
    # chuni_userはuserと結びついているため、バリデーションしない(contextで渡す)
    # チュウニズム側のプレイヤー名要件がかなりゆるいので形式については空文字以外はバリデーションしない

    chuni_player_name = serializers.CharField(
        max_length=20, write_only=True, required=True, allow_blank=False
    )

    def validate(self, attrs):
        if self.context["user"].chuni_user is None:
            raise serializers.ValidationError("チュウニズムのユーザーが存在しません。")
        return attrs

    def update(self, instance, validated_data):
        ChuniUserEx.update_chuni_player_name(
            instance, validated_data["chuni_player_name"]
        )
        return Response({"message": "ユーザー情報の更新が完了しました。"}, status=200)


class CreateChuniUserSerializer(serializers.Serializer):
    chuni_player_name = serializers.CharField(
        max_length=20, write_only=True, required=True, allow_blank=False
    )

    def validate(self, attrs):
        user = self.context["user"]
        if user.chuni_user is not None:
            raise serializers.ValidationError(
                "すでにチュウニズムのプレイヤー名が登録されています。"
            )
        return attrs

    def create(self, validated_data):
        user = self.context["user"]
        ChuniUserEx.create_chuni_user(user, validated_data["chuni_player_name"])
        return Response({"message": "ユーザー情報の更新が完了しました。"}, status=200)
