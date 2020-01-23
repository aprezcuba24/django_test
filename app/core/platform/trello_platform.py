from ..models import PlatformType
from .base import BasePlatform


class TrelloPlatform(BasePlatform):
    def get_name(self):
        return PlatformType.TRELLO.label

    def get_oaut_url(self):
        return 'trello oauth'
