
from chuniscore_recorder.models.proxy import UserEx
from rest_framework import serializers

from chuniscore_recorder.utils.auth_util import AuthUtilEx


class TokenObtainPairSerializerForUser(serializers.Serializer):

    name = serializers.CharField(max_length=20, write_only=True)
    password = serializers.CharField(write_only=True)

    def validate_user_name(self, value):
        if value is None:
            raise serializers.ValidationError('name is required.')
        return value

    def validate_password(self, value):
        if value is None:
            raise serializers.ValidationError('password is required.')
        return value

    def to_representation(self, instance):
        token = AuthUtilEx.create_token(instance.name)
        return {'token': token.decode()}

    def create(self, validated_data):
        if not UserEx.get_user_permission(validated_data['name'], validated_data['password']):
            raise serializers.ValidationError('User authentication failed.')
        user = UserEx.objects.get(name=validated_data['name'])
        return user

