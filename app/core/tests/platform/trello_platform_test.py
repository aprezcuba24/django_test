import json
from unittest.mock import MagicMock
import requests
from django.test import TestCase
from django.conf import settings
from app.core.platform import TrelloPlatform
from app.core.models import PlatformType, Board
from app.users.models import User


class RequestMock:
    GET = dict(
        token='token',
    )

def create_response_mock(username):
    class ResponseMock:
        content = json.dumps(dict(
            username=username,
        ))
    return ResponseMock

class TrelloPlatformTest(TestCase):
    def test_login(self):
        assert User.objects.all().count() == 0
        requests.get = MagicMock(return_value=create_response_mock('username1'))

        request = RequestMock()
        platform = TrelloPlatform(
            django_login=lambda x, y: None,
            Board=Board,
            User=User,
            requests=requests,
            settings=settings,
        )
        assert PlatformType.TRELLO == platform.get_type()

        user = platform.login(request)
        assert User.objects.all().count() == 1
        assert user.username == 'username1'
        assert user.platform == PlatformType.TRELLO
        assert user.platform_integration['token'] == 'token'

        # If the response returns the same username, the system doesn't create another.
        other = platform.login(request)
        assert User.objects.all().count() == 1
        assert user.id == other.id

        # Now the response mock will return another username, a new user will be created. 
        requests.get = MagicMock(return_value=create_response_mock('username2'))
        user = platform.login(request)
        assert User.objects.all().count() == 2
        assert user.username == 'username2'
