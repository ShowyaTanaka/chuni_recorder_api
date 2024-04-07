from datetime import datetime

import jwt

from config.settings import settings


class AuthUtilEx:
    @classmethod
    def create_token(cls, user_name):
        payload = {
            'name': user_name,
            'until': (datetime.now() + settings.TOKEN_LIFETIME).timestamp()
        }
        key = settings.SECRET_KEY
        token = jwt.encode(
            payload=payload,
            key=key,
            algorithm="HS256"
        )
        return token