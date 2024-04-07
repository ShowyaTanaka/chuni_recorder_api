from chuniscore_recorder.views.auth import AuthUserLoginView, AuthUserJWTOperateView, AuthUserCheckView
from django.urls import path, include
from rest_framework.routers import SimpleRouter
router = SimpleRouter()
router.register('auth/login', AuthUserLoginView, basename='auth_user_login')

router.register('auth', AuthUserJWTOperateView, basename='auth_user_jwt')


urlpatterns = [
    path('auth/check/', AuthUserCheckView.as_view()),
    path('', include(router.urls)),

]
