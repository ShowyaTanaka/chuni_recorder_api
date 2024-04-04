from chuniscore_recorder.views.auth_user_view import AuthUserView
from django.urls import path, include
from rest_framework.routers import SimpleRouter
router = SimpleRouter()
router.register('auth', AuthUserView, basename='auth_user')

urlpatterns = [
    path('', include(router.urls))
]
