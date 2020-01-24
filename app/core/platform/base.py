from django.contrib.auth import login as django_login
from app.core.models import Board, Group, Card


class BasePlatform:
    def get_name(self):
        raise NotImplementedError

    def get_oaut_url(self):
        raise NotImplementedError

    def login(self, request):
        user = self._find_or_create(request)
        django_login(request, user)
        return user

    def _find_or_create(self, request):
        raise NotImplementedError

    def load_all(self, user):
        Board.objects.get_by_user(user).delete()
        boards = self._load_boards(user)
        groups = self._load_lists(user, boards)
        self._load_cards(user, groups)

    def _load_boards(self, user):
        raise NotImplementedError

    def _load_lists(self, user, boards):
        raise NotImplementedError

    def _load_cards(self, user, groups):
        raise NotImplementedError
