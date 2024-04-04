import unittest

from django.http import SimpleCookie
from django.test import Client
from chuniscore_recorder.models import User
import pytest

class AuthUserTest(unittest.TestCase):

    """
    ユーザー認証のテストを行う。
    対応url: /auth/
    本来であればView,Serializerも個別にテストを行うべきであるが,今回の規模ならばエンドポイント単位のテストで十分であると判断した。
    """

    @classmethod
    def _set_cookie(cls, client, response):
        client.cookies = SimpleCookie({'token': response.cookies.get('token')})

    def setUp(self):
        User.create_user('test', 'password')

    @pytest.mark.django_db
    def test_post(self):
        with self.subTest("正しいユーザー名,pwの場合,ユーザー認証が成功する"):
            client = Client()
            response = client.post('/auth/login/', {'name': 'test', 'password': 'password'})
            self.assertEqual(response.status_code, 200)
        with self.subTest("誤ったユーザー名の場合,ユーザー認証が失敗する"):
            client = Client()
            response = client.post('/auth/login/', {'name': 'test', 'password': 'wrong_password'})
            self.assertEqual(response.status_code, 400)
        with self.subTest("誤ったパスワードの場合,ユーザー認証が失敗する"):
            client = Client()
            response = client.post('/auth/login/', {'name': 'test', 'password': 'password__'})
            self.assertEqual(response.status_code, 400)
        with self.subTest("存在しないユーザー名の場合,ユーザー認証が失敗する"):
            client = Client()
            response = client.post('/auth/login/', {'name': 'test_', 'password': 'password'})
            self.assertEqual(response.status_code, 400)
        with self.subTest("ユーザー名が空の場合,ユーザー認証が失敗する"):
            client = Client()
            response = client.post('/auth/login/', {'name': '', 'password': 'password'})
            self.assertEqual(response.status_code, 400)
        with self.subTest("ユーザー名がない場合,ユーザー認証が失敗する"):
            client = Client()
            response = client.post('/auth/login/', {'password': 'password'})
            self.assertEqual(response.status_code, 400)
        with self.subTest("パスワードが空の場合,ユーザー認証が失敗する"):
            client = Client()
            response = client.post('/auth/login/', {'name': 'test', 'password': ''})
            self.assertEqual(response.status_code, 400)
        with self.subTest("パスワードがない場合,ユーザー認証が失敗する"):
            client = Client()
            response = client.post('/auth/login/', {'name': 'test'})
            self.assertEqual(response.status_code, 400)

    @pytest.mark.freeze_time('2022-01-01')
    def token_at_2022_01_01(self):
        client = Client()
        response = client.post('/auth/login/', {'name': 'test', 'password': 'password'})
        return response

    @pytest.mark.django_db
    def test_refresh(self):
        with self.subTest("トークンが存在する場合,トークンを更新する"):
            client = Client()
            response = client.post('/auth/login/', {'name': 'test', 'password': 'password'})
            self._set_cookie(response, client)
            response = client.get('/auth/refresh/')
            self.assertEqual(response.status_code, 200)
        with self.subTest("トークンが存在しない場合,トークンを更新しない"):
            client = Client()
            response = client.get('/auth/refresh/')
            self._set_cookie(response, client)
            self.assertEqual(response.status_code, 400)

        with self.subTest("トークンが不正な場合,トークンを更新しない"):
            client = Client()
            response = client.post('/auth/login/', {'name': 'test', 'password': 'password'})
            response.cookies['token'] = 'wrong_token'
            self._set_cookie(response, client)
            response = client.get('/auth/refresh/')
            self.assertEqual(response.status_code, 400)

        with self.subTest("トークンが期限切れの場合,トークンを更新しない"):
            client = Client()
            response = self.token_at_2022_01_01()
            self._set_cookie(response, client)
            response = client.get('/auth/refresh/')
            self.assertEqual(response.status_code, 400)

    @pytest.mark.django_db
    def test_check_token(self):
        with self.subTest("トークンが存在する場合,トークンが有効か確認する"):
            client = Client()
            response = client.post('/auth/login/', {'name': 'test', 'password': 'password'})
            self._set_cookie(response, client)
            response = client.get('/auth/check/')
            self.assertEqual(response.json(), {'is_authenticated': True})
        with self.subTest("トークンが存在しない場合,トークンが有効出ないことを示す"):
            client = Client()
            response = client.get('/auth/check/')
            self.assertEqual(response.json(), {'is_authenticated': False})
        with self.subTest("トークンが不正な場合,トークンが有効出ないことを示す"):
            client = Client()
            response = client.post('/auth/login/', {'name': 'test', 'password': 'password'})
            response.cookies['token'] = 'wrong_token'
            self._set_cookie(response, client)
            response = client.get('/auth/check/')
            self.assertEqual(response.json(), {'is_authenticated': False})
        with self.subTest("トークンが期限切れの場合,トークンが有効出ないことを示す"):
            client = Client()
            response = self.token_at_2022_01_01()
            self._set_cookie(response, client)
            response = client.get('/auth/check/')
            self.assertEqual(response.json(), {'is_authenticated': False})