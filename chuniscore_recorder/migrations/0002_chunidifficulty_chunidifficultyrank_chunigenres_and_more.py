# Generated by Django 4.2.11 on 2024-04-08 13:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("chuniscore_recorder", "0001_initial"),
    ]

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
            name="ChuniGenres",
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
            name="ChuniMusics",
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
                        to="chuniscore_recorder.chunigenres",
                    ),
                ),
            ],
            options={
                "db_table": "chuni_musics",
            },
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
        migrations.AddField(
            model_name="user",
            name="chuni_user_name",
            field=models.CharField(
                help_text="チュウニズムのプレイヤー名", max_length=255, null=True
            ),
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
                ("play_date", models.DateField(help_text="プレイ日")),
                (
                    "difficulty",
                    models.ForeignKey(
                        help_text="難易度",
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="result_difficulty",
                        to="chuniscore_recorder.chunidifficulty",
                    ),
                ),
                (
                    "music",
                    models.ForeignKey(
                        help_text="曲名",
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="result_music",
                        to="chuniscore_recorder.chunimusics",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        help_text="ユーザー名",
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="result_user",
                        to="chuniscore_recorder.user",
                    ),
                ),
            ],
            options={
                "db_table": "chuni_result",
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
                to="chuniscore_recorder.chunimusics",
            ),
        ),
    ]
