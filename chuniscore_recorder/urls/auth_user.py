from chuniscore_recorder.views.auth_user_view import AuthUserView
from django.urls import path

urlpatterns = [
    path('/auth', AuthUserView, name='auth'),
]
