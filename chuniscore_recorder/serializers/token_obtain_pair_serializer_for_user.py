
from chuniscore_recorder.models import User
from rest_framework import serializers


class TokenObtainPairSerializerForUser(serializers.Serializer):


    def validate(self, data):
        data = self.context['request'].data
        if (data.get('name', None) is None) or (data.get('password', None) is None):
            raise serializers.ValidationError('name and password are required.')
        if not User.get_user_permission(data['name'], data['password']):
            raise serializers.ValidationError('name or password is incorrect.')
        return super().validate(data)

