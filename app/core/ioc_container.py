from dependency_injector import providers, containers
from .platform import TrelloPlatform
from app.core.models import PlatformType


class Container(containers.DeclarativeContainer):
    platform_trello = providers.Singleton(TrelloPlatform)

    @classmethod
    def get_platform(cls, platform_type):
        factory_name = f'platform_{platform_type.label.lower()}'
        factory = getattr(cls, factory_name)
        return factory()

    @classmethod
    def get_platforms(cls):
        platforms = []
        for item in PlatformType:
            platforms.append(cls.get_platform(item))
        return platforms
