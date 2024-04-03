from chuniscore_recorder.models.user import User
from django.contrib.auth.hashers import check_password

class UserEx(User):
    class Meta:
        proxy = True

