from chuniscore_recorder.views.chuni_musics import ChuniMusicViewSet
from django.urls import path, include
from rest_framework.routers import SimpleRouter
router = SimpleRouter()
router.register('chuni_musics', ChuniMusicViewSet, basename='chuni_music')
urlpatterns = [
    path('', include(router.urls)),
]