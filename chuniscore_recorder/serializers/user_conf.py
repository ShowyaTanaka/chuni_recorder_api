import re
from datetime import datetime

import jwt
from rest_framework import serializers
from rest_framework.response import Response

from chuniscore_recorder.models.proxy.userex import UserEx
from chuniscore_recorder.utils.auth_util import AuthUtilEx
from chuniscore_recorder.models.proxy.chuniuserex import ChuniUserEx


class CreateUserSerializer(serializers.Serializer):

    user_name = serializers.CharField(max_length=20, write_only=True)
    password = serializers.CharField(write_only=True)

    def validate_user_name(self, value):
        if value is None:
            raise serializers.ValidationError('ユーザー名は必須です。')
        if not value.isalnum():
            raise serializers.ValidationError('ユーザー名は半角英数字である必要があります。')
        if UserEx.is_user_name_exist(value):
            raise serializers.ValidationError('既に存在するユーザー名です。ほかのユーザー名を利用してください。')
        return value

    def validate_password(self, value):
        password_condition = re.compile(r'^[a-zA-Z0-9_ ]+$')
        if not password_condition.match(value):
            raise serializers.ValidationError('パスワードは半角英数字,アンダーバー,スペースからなる必要があります。')
        if value is None:
            raise serializers.ValidationError('パスワードは必須です。')
        if len(value) < 6:
            raise serializers.ValidationError('パスワードは6文字以上である必要があります。')
        return value

    def to_representation(self, instance):
        token = AuthUtilEx.create_token(instance.name)
        return {'token': token.decode()}

    def create(self, validated_data):
        user = UserEx.create_user(validated_data['user_name'], validated_data['password'])
        return user

class UpdateChuniUserSerializer(serializers.Serializer):
    # chuni_userはuserと結びついているため、バリデーションしない(contextで渡す)

    chuni_player_name = serializers.CharField(max_length=20, write_only=True, required=True)

    def update(self, instance, validated_data):
        user = UserEx.objects.get(name=self.context['user_name'])
        ChuniUserEx.update_chuni_player_name(user, validated_data['chuni_player_name'])
        return Response({'message': 'ユーザー情報の更新が完了しました。'}, status=200)