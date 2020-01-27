import requests as requests_handler
from dependency_injector import providers, containers
from django.contrib.auth import login as django_login
from django.contrib.auth import get_user_model
from django.conf import settings as django_settings
from app.core.models import PlatformType, Board, Group, Card
from .platform import TrelloPlatform


class Container(containers.DeclarativeContainer):
    user = providers.Object(get_user_model())
    login = providers.Object(django_login)
    requests = providers.Object(requests_handler)
    board_model = providers.Object(Board)
    group_model = providers.Object(Group)
    card_model = providers.Object(Card)
    settings = providers.Object(django_settings)
    platform_trello = providers.Singleton(
        TrelloPlatform,
        django_login=login,
        requests=requests,
        Board=board_model,
        Group=group_model,
        Card=card_model,
        settings=settings,
        User=user,
    )

    @classmethod
    def get_platform(cls, platform_type):
        if not isinstance(platform_type, str):
            platform_type = platform_type.label.lower()
        factory_name = f'platform_{platform_type}'
        factory = getattr(cls, factory_name)
        return factory()

    @classmethod
    def get_platforms(cls):
        platforms = []
        for item in PlatformType:
            platforms.append(cls.get_platform(item))
        return platforms
