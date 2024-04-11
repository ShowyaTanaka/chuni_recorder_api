from .base import *


SPECTACULAR_SETTINGS = {
    'TITLE': 'chuniscore_recorder API',
    'DESCRIPTION': '詳細',
    'VERSION': '1.0.0',
    # api/schemaを表示しない
    'SERVE_INCLUDE_SCHEMA': False,
}

INSTALLED_APPS += [
    "drf_spectacular",
    "debug_toolbar"
]
MIDDLEWARE += [
    # ...
    'debug_toolbar.middleware.DebugToolbarMiddleware',  # 追加
]

# 追加
INTERNAL_IPS = ['127.0.0.1']

# 追加
DEBUG_TOOLBAR_CONFIG = {
    "SHOW_TOOLBAR_CALLBACK" : lambda request: True,
}
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'