from chuniscore_recorder.views.auth_user import AuthBaseViewSet
from django.urls import path

urlpatterns = [
    path('auth/', AuthBaseViewSet, name='auth'),
]
