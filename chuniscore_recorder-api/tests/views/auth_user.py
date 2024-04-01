import unittest
from chuniscore_recorder.views.auth_user import AuthBaseViewSet
from django.test import Client
import pytest

class AuthBaseViewSetTest(unittest.TestCase):
    def test_post(self):
        client = Client()
        response = client.post('/auth/', {'name': 'test', 'password': 'password'})