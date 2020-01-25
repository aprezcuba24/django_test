import json
from ..models import PlatformType
from .base import BasePlatform

class TrelloPlatform(BasePlatform):

    API_URL = 'https://api.trello.com/1'

    def get_type(self):
        return PlatformType.TRELLO

    def get_oaut_url(self):
        return f'https://trello.com/1/authorize?expiration=1day&scope=read&response_type=token&key={self.settings.TRELLO_KEY}&return_url={self.settings.TRELLO_URL_REDIRECT}'

    def _set_connection_params(self, user):
        self.connection_params['key'] = self.settings.TRELLO_KEY
        if isinstance(user, str):
            self.connection_params['token'] = user
        else:
            self.connection_params['token'] = user.platform_integration['token']

    def _find_or_create(self, request):
        '''
        The token is diferent in each login and expires in one day.
        '''
        token = request.GET.get('token')
        if not token:
            raise ValueError('The token is not exists.')
        self._set_connection_params(token)
        response = self.requests.get(self._get_api_url('/members/me/'))
        data = json.loads(response.content)
        try:
            return self.User.objects.get(
                username=data['username'],
            )
        except self.User.DoesNotExist:
            return self._create_user(
                username=data['username'],
                platform_integration=dict(
                    token=token,
                )
            )

    def _get_boards_from_platform(self):
        return self.requests.get(
            self._get_api_url('/members/me/boards')
        )

    def _get_groups_from_platform(self, board):
        return self.requests.get(self._get_api_url(
            f'/boards/{board.data["id"]}',
            lists='all',
            list_fields='all',
            fields='name',
        ))

    def _get_cards_from_platform(self, group):
        return self.requests.get(self._get_api_url(
            f'/lists/{group.data["id"]}/cards/',
            fields='all',
        ))
