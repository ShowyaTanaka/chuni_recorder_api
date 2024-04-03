import unittest
from chuniscore_recorder.models.user import User
import pytest

@pytest.mark.django_db
class TestUser(unittest.TestCase):
    def test_password(self):
        with self.subTest("パスワード認証に基づいて,ユーザーを作成できる"):
            User.create_user("test", "password")
            user = User.objects.get(name="test")
            self.assertEqual(user.name, "test")

        with self.subTest("同一のユーザー名でユーザーを作成できない"):
            with self.assertRaises(Exception):
                User.create_user("test", "password")


        with self.subTest("パスワード認証に基づいて,ユーザーを取得できる"):
            user = User.get_user_permission("test", "password")
            self.assertEqual(user.name, "test")

        with self.subTest("存在しないユーザー名でユーザーを取得できない"):
            user = User.get_user_permission("test2", "password")
            self.assertEqual(user, None)

        with self.subTest("パスワードが違うユーザーを取得できない"):
            user = User.get_user_permission("test", "password2")
            self.assertEqual(user, False)

