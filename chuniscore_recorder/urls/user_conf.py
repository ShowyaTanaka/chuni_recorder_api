from chuniscore_recorder.views.user_conf import UserConfigCreateViewSet
from django.urls import path, include
from rest_framework.routers import SimpleRouter
router = SimpleRouter()
router.register('user_conf/new', UserConfigCreateViewSet, basename='user_conf_create')
urlpatterns = [
    path('', include(router.urls)),
]