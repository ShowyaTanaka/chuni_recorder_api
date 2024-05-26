import pytest
from django.test import Client
from django.test import TestCase

from chuniscore_recorder.models import ChuniResult


class ChuniScoreTest(TestCase):
    fixtures = [
        "tests/fixtures/endpoint/chuni_score/chuni_difficulty.json",
        "tests/fixtures/endpoint/chuni_score/chuni_difficulty_rank.json",
        "tests/fixtures/endpoint/chuni_score/user.json",
        "tests/fixtures/endpoint/chuni_score/chuni_music.json",
        "tests/fixtures/endpoint/chuni_score/chuni_user.json",
        "tests/fixtures/endpoint/chuni_score/chuni_result.json",
    ]
    maxDiff = None

    def _generate_jwt_token(self, user_name):
        from datetime import datetime, timedelta
        import jwt
        from django.conf import settings

        payload = {
            "name": user_name,
            "until": str(datetime.now() + timedelta(days=1)),
        }
        return jwt.encode(payload, key=settings.SECRET_KEY, algorithm="HS256")

    @pytest.mark.django_db
    def test_chuni_score_list(self):
        with self.subTest("IDをつけて検索した際,そのIDのリザルト一覧を取得できる。"):
            client = Client()
            response = client.get("/chuni_score/get_score/user1/")
            self.assertEqual(response.status_code, 200)
            self.assertEqual(
                {
                    "result": [
                        {
                            "difficulty": "MASTER",
                            "music_title": "Ultimate Force",
                            "score": 965000,
                            "constant": "15.0",
                            "registered_time": "2024-04-26T20:00:00Z",
                        },
                        {
                            "difficulty": "MASTER",
                            "music_title": "Aleph-0",
                            "score": 975000,
                            "constant": "15.0",
                            "registered_time": "2024-04-25T20:00:00Z",
                        },
                    ],
                    "player_name": "user1",
                },
                response.json(),
            )

    @pytest.mark.django_db
    @pytest.mark.freeze_time("2024-04-27")
    def test_chuni_result_post(self):
        with self.subTest("スコアを登録することができる。"):
            client = Client()
            from chuniscore_recorder.utils.auth_util import AuthUtilEx

            token = AuthUtilEx.create_token("user2")
            response = client.post(
                "/chuni_score/register_score/",
                {
                    "score_list": [
                        {"music_id": 1, "difficulty": "MASTER", "score": 1000000},
                        {"music_id": 2, "difficulty": "MASTER", "score": 1000000},
                    ]
                },
                content_type="application/json",
                headers={"Token": token},
            )
            self.assertEqual(response.status_code, 200)
            self.assertEqual(
                ChuniResult.objects.filter(chuni_user__player_name="user2").count(), 2
            )
        with self.subTest(
            "すでに登録されている曲の場合、スコアが低いリザルトは登録しない。"
        ):
            response = client.post(
                "/chuni_score/register_score/",
                {
                    "score_list": [
                        {"music_id": 1, "difficulty": "MASTER", "score": 900000},
                    ]
                },
                content_type="application/json",
                headers={"Token": token},
            )
            self.assertEqual(response.status_code, 200)
            self.assertEqual(
                ChuniResult.objects.filter(chuni_user__player_name="user2").count(), 2
            )
        with self.subTest(
            "すでに登録されている曲の場合、スコアが高いリザルトは登録する。"
        ):
            response = client.post(
                "/chuni_score/register_score/",
                {
                    "score_list": [
                        {"music_id": 1, "difficulty": "MASTER", "score": 1000001},
                    ]
                },
                content_type="application/json",
                headers={"Token": token},
            )
            self.assertEqual(response.status_code, 200)
            self.assertEqual(
                ChuniResult.objects.filter(chuni_user__player_name="user2").count(), 3
            )
