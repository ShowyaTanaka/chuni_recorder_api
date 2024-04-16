import datetime
import unittest
from datetime import time

from django.http.cookie import SimpleCookie
from django.test import Client
from chuniscore_recorder.models.proxy import UserEx, ChuniUserEx
import pytest
from django.conf import settings
import jwt


class AuthUserTest(unittest.TestCase):
    """
    ユーザー認証のテストを行う。
    対応url: /auth/
    本来であればView,Serializerも個別にテストを行うべきであるが,今回の規模ならばエンドポイント単位のテストで十分であると判断した。
    """

    def setUp(self):
        UserEx.create_user("test", "password")

    @pytest.mark.django_db
    def test_post(self):
        with self.subTest("正しいユーザー名,pwの場合,ユーザー認証が成功する"):
            client = Client()
            response = client.post(
                "/auth/login/", {"user_name": "test", "password": "password"}
            )
            self.assertEqual(response.status_code, 200)
            name = jwt.decode(
                response.json().get("token"), settings.SECRET_KEY, algorithms=["HS256"]
            ).get("name")
            self.assertEqual(name, "test")
        with self.subTest("誤ったユーザー名の場合,ユーザー認証が失敗する"):
            client = Client()
            response = client.post(
                "/auth/login/", {"user_name": "test", "password": "wrong_password"}
            )
            self.assertEqual(response.status_code, 400)
        with self.subTest("誤ったパスワードの場合,ユーザー認証が失敗する"):
            client = Client()
            response = client.post(
                "/auth/login/", {"user_name": "test", "password": "password__"}
            )
            self.assertEqual(response.status_code, 400)
        with self.subTest("存在しないユーザー名の場合,ユーザー認証が失敗する"):
            client = Client()
            response = client.post(
                "/auth/login/", {"user_name": "test_", "password": "password"}
            )
            self.assertEqual(response.status_code, 400)
        with self.subTest("ユーザー名が空の場合,ユーザー認証が失敗する"):
            client = Client()
            response = client.post(
                "/auth/login/", {"user_name": "", "password": "password"}
            )
            self.assertEqual(response.status_code, 400)
        with self.subTest("ユーザー名がない場合,ユーザー認証が失敗する"):
            client = Client()
            response = client.post("/auth/login/", {"password": "password"})
            self.assertEqual(response.status_code, 400)
        with self.subTest("パスワードが空の場合,ユーザー認証が失敗する"):
            client = Client()
            response = client.post(
                "/auth/login/", {"user_name": "test", "password": ""}
            )
            self.assertEqual(response.status_code, 400)
        with self.subTest("パスワードがない場合,ユーザー認証が失敗する"):
            client = Client()
            response = client.post("/auth/login/", {"user_name": "test"})
            self.assertEqual(response.status_code, 400)

    def token_at_2022_01_01(self):
        payload = {
            "name": "test",
            "until": datetime.datetime(year=2022, month=1, day=1).timestamp(),
        }
        jwt_token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
        return jwt_token.decode()

    def _refresh_token_at_2022_01_01(self):
        token = UserEx.create_refresh_token(UserEx.objects.get(name="test"))
        UserEx.objects.filter(name="test").update(
            refresh_token_updated_at=datetime.datetime(
                year=2022, month=1, day=1, hour=0, minute=0, second=0
            )
        )
        return token

    @pytest.mark.django_db
    def test_refresh(self):
        with self.subTest("トークンが存在する場合,トークンを更新する"):
            client = Client()
            response = client.post(
                "/auth/login/", {"user_name": "test", "password": "password"}
            )
            client.cookies = SimpleCookie(
                {"refresh_token": response.cookies.get("refresh_token").value}
            )
            previous_token_time = jwt.decode(
                response.json().get("token"), settings.SECRET_KEY, algorithms=["HS256"]
            ).get("until")
            response = client.get(
                "/auth/refresh/",
                headers={
                    "Token": response.json().get("token"),
                    "user_name": response.json().get("user_name"),
                },
            )
            self.assertEqual(response.status_code, 200)
            self.assertNotEqual(
                jwt.decode(
                    response.json().get("token"),
                    settings.SECRET_KEY,
                    algorithms=["HS256"],
                ).get("until"),
                previous_token_time,
            )
            self.assertEqual(
                jwt.decode(
                    response.json().get("token"),
                    settings.SECRET_KEY,
                    algorithms=["HS256"],
                ).get("name"),
                "test",
            )
        with self.subTest("トークンが存在しない場合,トークンを更新しない"):
            client = Client()
            response = client.get("/auth/refresh/")
            self.assertEqual(response.status_code, 403)
            self.assertEqual(response.json(), {"detail": "Refresh token is not found."})

        with self.subTest("トークンが不正な場合,トークンを更新しない"):
            client = Client()
            client.cookies = SimpleCookie({"refresh_token": "AA"})
            response = client.get("/auth/refresh/")
            self.assertEqual(response.status_code, 403)
            self.assertEqual(response.json(), {"detail": "Token is invalid."})

        with self.subTest("トークンが期限切れの場合,トークンを更新しない"):
            token = self._refresh_token_at_2022_01_01()
            client = Client()
            client.cookies = SimpleCookie({"refresh_token": token})
            response = client.get("/auth/refresh/", headers={"user_name": "test"})
            self.assertEqual(response.status_code, 403)
            self.assertEqual(response.json(), {"detail": "Token is expired."})

    @pytest.mark.django_db
    def test_check_token(self):
        with self.subTest("トークンが存在する場合,トークンが有効か確認する"):
            client = Client()
            response = client.post(
                "/auth/login/", {"user_name": "test", "password": "password"}
            )
            response = client.get(
                "/auth/check/", headers={"Token": response.json().get("token")}
            )
            self.assertEqual(response.json(), {"is_authenticated": True})
        with self.subTest("トークンが存在しない場合,トークンが有効出ないことを示す"):
            client = Client()
            response = client.get("/auth/check/")
            self.assertEqual(response.json(), {"is_authenticated": False})
        with self.subTest("トークンが不正な場合,トークンが有効出ないことを示す"):
            client = Client()
            response = client.get("/auth/check/", headers={"Token": "AA"})
            self.assertEqual(response.json(), {"is_authenticated": False})
        with self.subTest("トークンが期限切れの場合,トークンが有効出ないことを示す"):
            client = Client()
            token = self.token_at_2022_01_01()
            response = client.get("/auth/check/", headers={"Token": token})
            self.assertEqual(response.json(), {"is_authenticated": False})

    def _create_chuni_user(self):
        user = UserEx.objects.get(name="test")
        ChuniUserEx.create_chuni_user(name="test_chuni_user", user=user)

    @pytest.mark.django_db
    def test_status(self):
        with self.subTest("トークンが存在する場合,ユーザーのステータスを取得する"):
            client = Client()
            response = client.post(
                "/auth/login/", {"user_name": "test", "password": "password"}
            )
            response = client.get(
                "/auth/my_status/", headers={"Token": response.json().get("token")}
            )
            self.assertEqual(
                response.json(), {"user_name": "test", "chuni_player_name": None}
            )
        with self.subTest("トークンが存在しない場合,エラーを返す"):
            client = Client()
            response = client.get("/auth/my_status/")
            self.assertEqual(response.status_code, 403)
        with self.subTest("トークンが不正な場合,エラーを返す"):
            client = Client()
            response = client.get("/auth/my_status/", headers={"Token": "AA"})
            self.assertEqual(response.status_code, 403)
        with self.subTest("トークンが期限切れの場合,エラーを返す"):
            client = Client()
            token = self.token_at_2022_01_01()
            response = client.get("/auth/my_status/", headers={"Token": token})
            self.assertEqual(response.status_code, 403)
        with self.subTest(
            "チュウニズムユーザーが存在する場合,ユーザーのステータスを取得する"
        ):
            self._create_chuni_user()
            client = Client()
            response = client.post(
                "/auth/login/", {"user_name": "test", "password": "password"}
            )
            response = client.get(
                "/auth/my_status/", headers={"Token": response.json().get("token")}
            )
            self.assertEqual(
                response.json(),
                {"user_name": "test", "chuni_player_name": "test_chuni_user"},
            )
