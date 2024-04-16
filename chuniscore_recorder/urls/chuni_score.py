from chuniscore_recorder.views.chuni_score import ChuniScoreViewSet
from django.urls import path, include
from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register("chuni_score", ChuniScoreViewSet, basename="chuni_music")
urlpatterns = [
    path("", include(router.urls)),
]
