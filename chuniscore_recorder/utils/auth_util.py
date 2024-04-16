from datetime import datetime

import jwt

from config import settings


class AuthUtilEx:
    @classmethod
    def create_token(cls, user_name):
        payload = {
            "name": user_name,
            "until": (datetime.now() + settings.JWT_TOKEN_LIFETIME).timestamp(),
        }
        key = settings.SECRET_KEY
        token = jwt.encode(payload=payload, key=key, algorithm="HS256")
        return token
