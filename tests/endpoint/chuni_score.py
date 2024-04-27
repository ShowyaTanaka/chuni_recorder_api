import pytest
from django.test import Client
from django.test import TestCase


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

    @pytest.mark.django_db
    def test_chuni_score_list(self):
        with self.subTest("IDをつけて検索した際,そのIDのリザルト一覧を取得できる。"):
            client = Client()
            response = client.get("/chuni_score/1/get_score/")
            self.assertEqual(response.status_code, 200)
            self.assertEqual(
                [
                    {
                        "difficulty": "MASTER",
                        "music_id": 1,
                        "music_title": "Ultimate Force",
                        "score": 965000,
                        "constant": "15.0",
                        "registered_time": "2024-04-26T20:00:00Z",
                    },
                    {
                        "music_id": 2,
                        "difficulty": "MASTER",
                        "music_title": "Aleph-0",
                        "score": 975000,
                        "constant": "15.0",
                        "registered_time": "2024-04-25T20:00:00Z",
                    },
                ],
                response.json(),
            )
