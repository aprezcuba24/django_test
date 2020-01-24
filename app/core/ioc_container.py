from dependency_injector import providers, containers
from app.core.models import PlatformType
from .platform import TrelloPlatform


class Container(containers.DeclarativeContainer):
    platform_trello = providers.Singleton(TrelloPlatform)

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
