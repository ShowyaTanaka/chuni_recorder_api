from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from chuniscore_recorder.models import User


class TokenObtainPairSerializerForUser(TokenObtainPairSerializer):


    def validate(self, data):
        if (data.get('username', None) is None) or (data.get('password', None) is None):
            raise ValueError('username and password are required.')
        if not User.get_user_permission(data['username'], data['password']):
            raise ValueError('username or password is incorrect.')
        return super().validate(data)