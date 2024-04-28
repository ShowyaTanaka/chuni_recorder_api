from django.core.management.base import BaseCommand
import pandas as pd

from chuniscore_recorder.models import ChuniDifficulty, ChuniMusic, ChuniDifficultyRank


class Command(BaseCommand):
    help = "チュウニズムの楽曲情報を登録します。"

    def add_arguments(self, parser):
        parser.add_argument('--file-path', nargs=1, default='', type=str)

    def handle(self, *args, **options):
        if not options["file_path"]:
            print("ファイルパスを指定してください。")
            return
        file_path = options["file_path"][0]
        try:
            df = pd.read_csv(file_path)
        except FileNotFoundError:
            print("ファイルが見つかりません。")
            return
        except pd.errors.ParserError:
            print("ファイルが不正です。")
            return
        # すべての難易度を取得
        difficulties = ChuniDifficulty.objects.all().select_related("music")
        musics = set(difficulties.values_list("music__title", flat=True).distinct())
        difficulty_ranks = ChuniDifficultyRank.objects.all()
        # 曲名、難易度、定数が存在することを確認する。
        for index, row in df.iterrows():
            music_title = row["music_title"]
            difficulty = row["difficulty"]
            constant = row["constant"]
            if music_title is None or difficulty is None or constant is None:
                print("データが不正です。")
                return
        # 楽曲を登録する。
        music_array = []
        music_title_set = set()
        for index, row in df.iterrows():
            music_title = row["music_title"]
            if music_title not in musics:
                music_title_set.add(music_title)
        for music_title in music_title_set:
            music_array.append(ChuniMusic(title=music_title))
        ChuniMusic.objects.bulk_create(music_array)
        musics = ChuniMusic.objects.all()
        for index, row in df.iterrows():
            difficulty = row["difficulty"]
            if difficulty not in ["BASIC", "ADVANCED", "EXPERT", "MASTER", "ULTIMA", "WORLD'S END"]:
                print("難易度が不正です。")
                return
        create_list = []
        for index, row in df.iterrows():
            music_title = row["music_title"]
            difficulty = row["difficulty"]
            constant = row["constant"]
            difficulty_rank_qs = difficulty_ranks.get(difficulty_rank=difficulty)
            if difficulties.filter(
                music__title=music_title, difficulty_rank=difficulty_rank_qs
            ).exists():
                difficulties.get(
                    music__title=music_title, difficulty_rank=difficulty_rank_qs
                ).constant = constant
            else:
                create_list.append(
                    ChuniDifficulty(
                        music=musics.get(title=music_title),
                        difficulty_rank=difficulty_rank_qs,
                        constant=constant,
                    )
                )
        ChuniDifficulty.objects.bulk_create(create_list)
        ChuniDifficulty.objects.bulk_update(difficulties, ["constant"])
        print("楽曲情報を登録しました。")
