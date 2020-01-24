import json
import requests
from django.contrib.auth import get_user_model
from django.conf import settings
from ..models import PlatformType
from .base import BasePlatform


class TrelloPlatform(BasePlatform):

    TRELLO_API_URL = f'https://api.trello.com/1'

    def get_name(self):
        return PlatformType.TRELLO.label

    def get_oaut_url(self):
        return f'https://trello.com/1/authorize?expiration=1day&scope=read&response_type=token&key={settings.TRELLO_KEY}&return_url={settings.TRELLO_URL_REDIRECT}'

    def _get_api_url(self, uri, token):
        return f'{self.TRELLO_API_URL}{uri}?key={settings.TRELLO_KEY}&token={token}'

    def _find_or_create(self, request):
        token = request.GET.get('token')
        if not token:
            raise ValueError('The token is not exists.')
        User = get_user_model()
        response = requests.get(self._get_api_url('/members/me/', token))
        data = json.loads(response.content)
        try:
            user = User.objects.get(
                username=data['username']
            )
        except User.DoesNotExist:
            user = User(
                username=data['username'],
            )
        user.platform_integration = dict(
            token=token,
        )
        user.save()
        return user
