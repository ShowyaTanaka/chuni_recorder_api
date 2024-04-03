import unittest
from chuniscore_recorder.views.auth_user_view import AuthUserView
from django.test import Client
from chuniscore_recorder.models import User
import pytest

class AuthUserTest(unittest.TestCase):

    """
    ユーザー認証のテストを行う。
    対応url: /auth/
    本来であればView,Serializerも個別にテストを行うべきであるが,今回の規模ならばエンドポイント単位のテストで十分であると判断した。
    """

    def setUp(self):
        User.create_user('test', 'password')

    @pytest.mark.django_db
    def test_post(self):
        with self.subTest("正しいユーザー名,pwの場合,ユーザー認証が成功する"):
            client = Client()
            response = client.post('/auth/login', {'name': 'test', 'password': 'password'})
            self.assertEqual(response.status_code, 200)
        with self.subTest("誤ったユーザー名の場合,ユーザー認証が失敗する"):
            client = Client()
            response = client.post('/auth/login', {'name': 'test', 'password': 'wrong_password'})
            self.assertEqual(response.status_code, 400)
        with self.subTest("誤ったパスワードの場合,ユーザー認証が失敗する"):
            client = Client()
            response = client.post('/auth/login', {'name': 'test', 'password': 'password__'})
            self.assertEqual(response.status_code, 400)
        with self.subTest("存在しないユーザー名の場合,ユーザー認証が失敗する"):
            client = Client()
            response = client.post('/auth/login', {'name': 'test_', 'password': 'password'})
            self.assertEqual(response.status_code, 400)
        with self.subTest("ユーザー名が空の場合,ユーザー認証が失敗する"):
            client = Client()
            response = client.post('/auth/login', {'name': '', 'password': 'password'})
            self.assertEqual(response.status_code, 400)
        with self.subTest("ユーザー名がない場合,ユーザー認証が失敗する"):
            client = Client()
            response = client.post('/auth/login', {'password': 'password'})
            self.assertEqual(response.status_code, 400)
        with self.subTest("パスワードが空の場合,ユーザー認証が失敗する"):
            client = Client()
            response = client.post('/auth/login', {'name': 'test', 'password': ''})
            self.assertEqual(response.status_code, 400)
        with self.subTest("パスワードがない場合,ユーザー認証が失敗する"):
            client = Client()
            response = client.post('/auth/login', {'name': 'test'})
            self.assertEqual(response.status_code, 400)