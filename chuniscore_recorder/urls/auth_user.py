from chuniscore_recorder.views.auth import (
    AuthUserLoginView,
    AuthUserJWTOperateView,
    AuthUserCheckView,
    AuthUserJWTRefreshView,
)
from django.urls import path, include
from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register("auth", AuthUserLoginView, basename="auth_user_login")

router.register("auth", AuthUserJWTOperateView, basename="auth_user_jwt")
router.register("auth", AuthUserJWTRefreshView, basename="auth_user_tokens")


urlpatterns = [
    path("auth/check/", AuthUserCheckView.as_view()),
    path("", include(router.urls)),
]
