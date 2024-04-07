"""
URL configuration for chuniscore_recorder-api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    # 127.0.0.1/8000/api/schema にアクセスするとテキストファイルをダウンロードできます
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path('docs', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    # Redocの設定
    # 今回は127.0.0.1/8000/api/redoc にアクセスするとRedocが表示されるよう設定します
    path(
        "api/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
    path('', include('chuniscore_recorder.urls.auth_user')),
    path('', include('chuniscore_recorder.urls.user_conf')),
]
