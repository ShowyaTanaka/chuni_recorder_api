import unittest

from django.http import SimpleCookie
from django.test import Client
from chuniscore_recorder.models.proxy import UserEx
import pytest
import jwt
from django.conf import settings

from chuniscore_recorder.models.proxy.userex import UserEx


class UserConfTest(unittest.TestCase):
    """
    ユーザー設定のテストを行う。
    """

    @pytest.mark.django_db
    def test_create_user(self):
        with self.subTest(
            "PW,ユーザー名をPOSTすると,ユーザーが作成され,JWTトークンが返される"
        ):
            client = Client()
            response = client.post(
                "/user_conf/new/", {"user_name": "test", "password": "password"}
            )

            self.assertEqual(response.status_code, 201)
            self.assertEqual(UserEx.objects.filter(name="test").exists(), True)
            self.assertEqual(
                jwt.decode(
                    response.json().get("token").encode(),
                    settings.SECRET_KEY,
                    algorithms=["HS256"],
                )["name"],
                "test",
            )
