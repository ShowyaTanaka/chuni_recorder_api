import pytest
from django.test import Client
from django.test import TestCase


class ChuniMusicListTest(TestCase):
    fixtures = [
        "tests/fixtures/endpoint/chuni_music_list/chuni_music.json",
        "tests/fixtures/endpoint/chuni_music_list/chuni_difficulty_rank.json",
        "tests/fixtures/endpoint/chuni_music_list/chuni_difficulty.json",
    ]

    @pytest.mark.django_db
    def test_chuni_music_all_list(self):
        with self.subTest("条件をつけずに検索した際、全難易度のリストが取得できる。"):
            client = Client()
            response = client.get("/chuni_musics/")
            self.assertEqual(response.status_code, 200)
            self.assertEqual(
                [
                    {"id": 1, "music_title": "テスト楽曲1(ULT,WEなし)"},
                    {"id": 2, "music_title": "テスト楽曲2(WEなし,ULTあり)"},
                    {"id": 3, "music_title": "テスト楽曲3(WEあり,ULTなし)"},
                    {"id": 4, "music_title": "テスト楽曲4(WEあり,ULTあり)"},
                ],
                response.json(),
            )
        with self.subTest("WORLD'S ENDの難易度リストが取得できる。"):
            client = Client()
            response = client.get("/chuni_musics/?contain_worlds_end=true")
            self.assertEqual(response.status_code, 200)
            self.assertEqual(
                [
                    {"id": 3, "music_title": "テスト楽曲3(WEあり,ULTなし)"},
                    {"id": 4, "music_title": "テスト楽曲4(WEあり,ULTあり)"},
                ],
                response.json(),
            )
        with self.subTest("ULTIMAの難易度リストが取得できる。"):
            client = Client()
            response = client.get("/chuni_musics/?contain_ultima=true")
            self.assertEqual(response.status_code, 200)
            self.assertEqual(
                [
                    {"id": 2, "music_title": "テスト楽曲2(WEなし,ULTあり)"},
                    {"id": 4, "music_title": "テスト楽曲4(WEあり,ULTあり)"},
                ],
                response.json(),
            )
