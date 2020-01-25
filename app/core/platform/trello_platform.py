import json
from ..models import PlatformType, Board, Group, Card
from .base import BasePlatform

class TrelloPlatform(BasePlatform):

    API_URL = 'https://api.trello.com/1'

    def get_type(self):
        return PlatformType.TRELLO

    def get_oaut_url(self):
        return f'https://trello.com/1/authorize?expiration=1day&scope=read&response_type=token&key={self.settings.TRELLO_KEY}&return_url={self.settings.TRELLO_URL_REDIRECT}'

    def _get_api_url(self, uri, **kwargs):
        token = kwargs.get('token')
        if isinstance(token, self.User):
            kwargs['token'] = token.platform_integration['token']
        kwargs['key'] = self.settings.TRELLO_KEY
        return super()._get_api_url(uri, **kwargs)

    def _find_or_create(self, request):
        token = request.GET.get('token')
        if not token:
            raise ValueError('The token is not exists.')
        # The token is diferent in each login
        response = self.requests.get(self._get_api_url('/members/me/', token=token))
        data = json.loads(response.content)
        try:
            user = self.User.objects.get(
                username=data['username']
            )
        except self.User.DoesNotExist:
            user = self.User(
                username=data['username'],
                platform=PlatformType.TRELLO,
            )
        user.platform_integration = dict(
            token=token,
        )
        user.save()
        return user

    def _load_boards(self, user):
        response = self.requests.get(
            self._get_api_url('/members/me/boards', token=user)
        )
        items = json.loads(response.content)
        objects = []
        for item in items:
            objects.append(Board(
                name=item['name'],
                platform=PlatformType.TRELLO,
                user=user,
                data=item,
            ))
        Board.objects.bulk_create(objects)
        return objects

    def _load_lists(self, user, boards):
        objects = []
        for board in boards:
            response = self.requests.get(self._get_api_url(
                f'/boards/{board.data["id"]}',
                token=user,
                lists='all',
                list_fields='all',
                fields='name',
            ))
            items = json.loads(response.content)
            print(items)
            for item in items['lists']:
                objects.append(Group(
                    name=item['name'],
                    board=board,
                    data=item,
                ))
        Group.objects.bulk_create(objects)
        return objects

    def _load_cards(self, user, groups):
        objects = []
        for group in groups:
            response = self.requests.get(self._get_api_url(
                f'/lists/{group.data["id"]}/cards/',
                token=user,
                fields='all',
            ))
            items = json.loads(response.content)
            for item in items:
                objects.append(Card(
                    name=item['name'],
                    group=group,
                    data=item,
                ))
        Card.objects.bulk_create(objects)
        return objects
