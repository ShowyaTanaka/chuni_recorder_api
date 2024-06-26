# Generated by Django 4.2.11 on 2024-05-06 08:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="ChuniDifficulty",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("constant", models.FloatField(help_text="譜面定数")),
            ],
            options={
                "db_table": "chuni_difficulty",
            },
        ),
        migrations.CreateModel(
            name="ChuniDifficultyRank",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "difficulty_rank",
                    models.CharField(help_text="難易度ランク", max_length=20),
                ),
            ],
            options={
                "db_table": "chuni_difficulty_rank",
            },
        ),
        migrations.CreateModel(
            name="ChuniGenre",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "genre_name",
                    models.CharField(help_text="ジャンル名", max_length=255),
                ),
            ],
            options={
                "db_table": "chuni_genres",
            },
        ),
        migrations.CreateModel(
            name="ChuniUser",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "player_name",
                    models.CharField(help_text="プレイヤー名", max_length=255),
                ),
                (
                    "best_rating",
                    models.IntegerField(
                        blank=True, help_text="べ枠レーティング", null=True
                    ),
                ),
                (
                    "update_date",
                    models.DateTimeField(blank=True, help_text="更新日時", null=True),
                ),
            ],
            options={
                "db_table": "chuni_users",
            },
        ),
        migrations.CreateModel(
            name="User",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255, unique=True)),
                ("password", models.CharField(max_length=255)),
                (
                    "current_refresh_token",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "refresh_token_updated_at",
                    models.DateTimeField(blank=True, null=True),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "chuni_user",
                    models.OneToOneField(
                        blank=True,
                        help_text="チュウニズムのプレイヤー名",
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="user_chuni_user",
                        to="chuniscore_recorder.chuniuser",
                    ),
                ),
            ],
            options={
                "db_table": "users",
            },
        ),
        migrations.CreateModel(
            name="ChuniResult",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("score", models.IntegerField(help_text="スコア")),
                ("registered_time", models.DateTimeField(help_text="登録日")),
                (
                    "chuni_user",
                    models.ForeignKey(
                        help_text="ユーザー名",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="result_user",
                        to="chuniscore_recorder.chuniuser",
                    ),
                ),
                (
                    "music_difficulty",
                    models.ForeignKey(
                        help_text="曲名",
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="result_music",
                        to="chuniscore_recorder.chunidifficulty",
                    ),
                ),
            ],
            options={
                "db_table": "chuni_result",
            },
        ),
        migrations.CreateModel(
            name="ChuniMusic",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(help_text="曲名", max_length=255)),
                (
                    "genre_name",
                    models.ForeignKey(
                        blank=True,
                        help_text="ジャンル名",
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="chuni_musics_chuni_genres",
                        to="chuniscore_recorder.chunigenre",
                    ),
                ),
            ],
            options={
                "db_table": "chuni_musics",
            },
        ),
        migrations.AddField(
            model_name="chunidifficulty",
            name="difficulty_rank",
            field=models.ForeignKey(
                help_text="難易度",
                on_delete=django.db.models.deletion.PROTECT,
                related_name="chuni_difficulty_chuni_difficulty_rank",
                to="chuniscore_recorder.chunidifficultyrank",
            ),
        ),
        migrations.AddField(
            model_name="chunidifficulty",
            name="music",
            field=models.ForeignKey(
                help_text="曲名",
                on_delete=django.db.models.deletion.PROTECT,
                related_name="difficulty_music",
                to="chuniscore_recorder.chunimusic",
            ),
        ),
        migrations.CreateModel(
            name="ChuniResultEx",
            fields=[],
            options={
                "proxy": True,
                "indexes": [],
                "constraints": [],
            },
            bases=("chuniscore_recorder.chuniresult",),
        ),
        migrations.CreateModel(
            name="ChuniUserEx",
            fields=[],
            options={
                "proxy": True,
                "indexes": [],
                "constraints": [],
            },
            bases=("chuniscore_recorder.chuniuser",),
        ),
        migrations.CreateModel(
            name="UserEx",
            fields=[],
            options={
                "proxy": True,
                "indexes": [],
                "constraints": [],
            },
            bases=("chuniscore_recorder.user",),
        ),
    ]
