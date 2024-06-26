# Generated by Django 4.2.11 on 2024-04-28 11:27

from django.db import migrations


def insert_difficulty(apps, schema_editor):
    difficulty_rank = apps.get_model("chuniscore_recorder", "ChuniDifficultyRank")
    difficulties = ["BASIC", "ADVANCED", "EXPERT", "MASTER", "ULTIMA", "WORLD'S END"]
    for difficulty in difficulties:
        difficulty_rank.objects.create(difficulty_rank=difficulty)


class Migration(migrations.Migration):

    dependencies = [
        ("chuniscore_recorder", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(insert_difficulty),
    ]
