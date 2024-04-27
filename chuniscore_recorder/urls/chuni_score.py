from chuniscore_recorder.views.chuni_score import (
    ChuniScoreRegisterViewSet,
    ChuniScoreGetViewSet,
)
from django.urls import path, include
from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register(
    "chuni_score", ChuniScoreRegisterViewSet, basename="chuni_music_register"
)
router.register("chuni_score", ChuniScoreGetViewSet, basename="chuni_music_get")
urlpatterns = [
    path("", include(router.urls)),
]
