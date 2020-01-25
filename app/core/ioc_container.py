import requests
from dependency_injector import providers, containers
from django.contrib.auth import login as django_login
from django.contrib.auth import get_user_model
from django.conf import settings
from app.core.models import PlatformType, Board, Group, Card
from .platform import TrelloPlatform


class Container(containers.DeclarativeContainer):
    platform_trello = providers.Singleton(
        TrelloPlatform,
        django_login=django_login,
        requests=requests,
        Board=Board,
        Group=Group,
        Card=Card,
        settings=settings,
        User=get_user_model(),
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
