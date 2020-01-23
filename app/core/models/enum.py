from django_enumfield import enum


class PlatformType(enum.Enum):
    TRELLO = 1

    __labels__ = {
        TRELLO: 'TRELLO',
    }
