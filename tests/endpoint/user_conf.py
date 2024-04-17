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
                "/user_conf/new/", {"user_name": "test", "password": "#$DFG1234"}
            )
            print(response.json())

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
        with self.subTest("PWが数字のみの場合、エラーが発生する。"):
            client = Client()
            response = client.post(
                "/user_conf/new/", {"user_name": "test2", "password": "#123456"}
            )

            self.assertEqual(response.status_code, 400)
            self.assertEqual(UserEx.objects.filter(name="test2").exists(), False)

        with self.subTest("PWに全角文字が入力された場合、エラーが発生する。"):
            client = Client()
            response = client.post(
                "/user_conf/new/",
                {"user_name": "test3", "password": "あいうえおかきくけこ"},
            )

            self.assertEqual(response.status_code, 400)
            self.assertEqual(UserEx.objects.filter(name="test3").exists(), False)

        with self.subTest("PWが存在しない場合、エラーが発生する。"):
            client = Client()
            response = client.post("/user_conf/new/", {"user_name": "test4"})

            self.assertEqual(response.status_code, 400)
            self.assertEqual(UserEx.objects.filter(name="test4").exists(), False)

        with self.subTest("PWが空文字の場合、エラーが発生する。"):
            client = Client()
            response = client.post(
                "/user_conf/new/", {"user_name": "test5", "password": ""}
            )

            self.assertEqual(response.status_code, 400)
            self.assertEqual(UserEx.objects.filter(name="test5").exists(), False)

        with self.subTest("ユーザー名が空文字の場合、エラーが発生する。"):
            client = Client()
            response = client.post(
                "/user_conf/new/", {"user_name": "", "password": "#$DFG1234"}
            )

            self.assertEqual(response.status_code, 400)
            self.assertEqual(UserEx.objects.filter(name="").exists(), False)

        with self.subTest("ユーザー名が存在しない場合、エラーが発生する。"):
            client = Client()
            response = client.post("/user_conf/new/", {"password": "#$DFG1234"})

            self.assertEqual(response.status_code, 400)
            self.assertEqual(UserEx.objects.filter(name="").exists(), False)

        with self.subTest("ユーザー名が存在する場合、エラーが発生する。"):
            client = Client()
            response = client.post(
                "/user_conf/new/", {"user_name": "test", "password": "#$DFG1234"}
            )
            self.assertEqual(response.status_code, 400)
            self.assertEqual(UserEx.objects.filter(name="test").count(), 1)

        with self.subTest("ユーザー名が全角文字の場合、エラーが発生する。"):
            client = Client()
            response = client.post(
                "/user_conf/new/",
                {"user_name": "あいうえおかきくけこ", "password": "#$DFG1234"},
            )
            self.assertEqual(response.status_code, 400)
            self.assertEqual(
                UserEx.objects.filter(name="あいうえおかきくけこ").exists(), False
            )

    @pytest.mark.django_db
    def test_create_chuni_user(self):
        with self.subTest("ユーザーが存在しない場合、エラーが発生する。"):
            client = Client()
            response = client.post(
                "/user_conf/new_chuni_user/", {"chuni_player_name": "test"}
            )
            self.assertEqual(response.status_code, 403)
            self.assertEqual(UserEx.objects.filter(name="test").exists(), False)

        with self.subTest(
            "ユーザーが存在する場合、チュウニズムのユーザーが作成される。"
        ):
            client = Client()
            response = client.post(
                "/user_conf/new/", {"user_name": "test", "password": "#$DFG1234"}
            )
            token = response.json()["token"]
            response = client.post(
                "/user_conf/new_chuni_user/",
                {"chuni_player_name": "test"},
                headers={"Token": token},
            )
            self.assertEqual(response.status_code, 200)
            self.assertEqual(UserEx.objects.filter(name="test").exists(), True)
            self.assertEqual(
                UserEx.objects.get(name="test").chuni_user.player_name, "test"
            )
        with self.subTest(
            "チュウニズムのユーザーがすでに存在する場合、エラーが発生する。"
        ):
            client = Client()
            response = client.post(
                "/auth/login/", {"user_name": "test", "password": "#$DFG1234"}
            )
            token = response.json()["token"]
            response = client.post(
                "/user_conf/new_chuni_user/",
                {"chuni_player_name": "test"},
                headers={"Token": token},
            )
            self.assertEqual(response.status_code, 400)
        with self.subTest("全角文字を含んだプレイヤー名であっても作成できる。"):
            client = Client()
            response = client.post(
                "/user_conf/new/", {"user_name": "test2", "password": "#$DFG1234"}
            )
            token = response.json()["token"]
            response = client.post(
                "/user_conf/new_chuni_user/",
                {"chuni_player_name": "あいうえおかきくけこ"},
                headers={"Token": token},
            )
            self.assertEqual(response.status_code, 200)
            self.assertEqual(UserEx.objects.filter(name="test2").exists(), True)
            self.assertEqual(
                UserEx.objects.get(name="test2").chuni_user.player_name,
                "あいうえおかきくけこ",
            )
        with self.subTest("プレイヤー名が空文字の場合、エラーが発生する。"):
            client = Client()
            response = client.post(
                "/user_conf/new/", {"user_name": "test3", "password": "#$DFG1234"}
            )
            token = response.json()["token"]
            response = client.post(
                "/user_conf/new_chuni_user/",
                {"chuni_player_name": ""},
                headers={"Token": token},
            )
            self.assertEqual(response.status_code, 400)
