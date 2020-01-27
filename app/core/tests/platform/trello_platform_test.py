import json
from unittest.mock import MagicMock
from django.test import TestCase
from app.core.models import PlatformType, Board, Group, Card
from app.users.models import User
from app.core.ioc_container import Container


class RequestMock:
    GET = dict(
        token='token',
    )

def create_response_mock(data):
    class ResponseMock:
        content = json.dumps(data)
    return ResponseMock

class TrelloPlatformTest(TestCase):
    def setUp(self):
        Container.login.override(lambda x, y: None)
        self.requests = Container.requests()
        self.platform = Container.get_platform(PlatformType.TRELLO)

    def test_login(self):
        assert User.objects.all().count() == 0
        self.requests.get = MagicMock(return_value=create_response_mock(dict(
            username='username1',
        )))

        request = RequestMock()
        assert PlatformType.TRELLO == self.platform.get_type()

        user = self.platform.login(request)
        assert User.objects.all().count() == 1
        assert user.username == 'username1'
        assert user.platform == PlatformType.TRELLO
        assert user.platform_integration['token'] == 'token'

        # If the response returns the same username, the system doesn't create another.
        other = self.platform.login(request)
        assert User.objects.all().count() == 1
        assert user.id == other.id

        # Now the response mock will return another username, a new user will be created.
        self.requests.get = MagicMock(return_value=create_response_mock(dict(
            username='username2',
        )))
        user = self.platform.login(request)
        assert User.objects.all().count() == 2
        assert user.username == 'username2'

    def test_load(self):
        user = User.objects.create(
            username='username1',
            platform_integration=dict(
                token='token',
            ),
        )
        assert Board.objects.all().count() == 0
        self.requests.get = MagicMock()
        self.requests.get.side_effect = [
            create_response_mock([ # It returns the boards
                dict(
                    name='board1',
                    id='1',
                ),
                dict(
                    name='board2',
                    id='2',
                )
            ]),
            create_response_mock(dict( # It returns the lists of the first board.
                lists=[
                    dict(
                        name='list1',
                        id='1',
                    )
                ]
            )),
            create_response_mock(dict( # The second board doesn't have lists.
                lists=[],
            )),
            create_response_mock([ # The cards of the first board's list.
                dict(
                    name='card1',
                    id='1',
                ),
            ]),
        ]
        self.platform.load_all(user)

        assert Board.objects.all().count() == 2
        assert Group.objects.all().count() == 1
        assert Card.objects.all().count() == 1
        assert Group.objects.filter(
            board__name='board1'
        ).count() == 1
        assert Card.objects.filter(
            group__name='list1'
        ).count() == 1
