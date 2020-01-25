import json


class BasePlatform:
    API_URL = ''

    def __init__(self, django_login, Board, User, requests, settings, Group, Card):
        self.django_login = django_login
        self.Board = Board
        self.User = User
        self.Group = Group
        self.Card = Card
        self.requests = requests
        self.settings = settings
        self.connection_params = {}

    def get_name(self):
        return self.get_type().label

    def get_type(self):
        raise NotImplementedError

    def get_oaut_url(self):
        raise NotImplementedError

    def _get_api_url(self, uri, **kwargs):
        params = {**self.connection_params, **kwargs}
        params = [f'{item[0]}={item[1]}' for item in params.items()]
        params = '&'.join(params)
        return f'{self.API_URL}{uri}?{params}'

    def login(self, request):
        user = self._find_or_create(request)
        self.django_login(request, user)
        return user

    def _find_or_create(self, request):
        raise NotImplementedError

    def load_all(self, user):
        self._set_connection_params(user)
        self.Board.objects.get_by_user(user).delete()
        boards = self._load_boards(user)
        groups = self._load_lists(boards)
        self._load_cards(groups)

    def _set_connection_params(self, user):
        pass

    def _load_boards(self, user):
        response = self._get_boards_from_platform()
        items = json.loads(response.content)
        objects = []
        for item in items:
            objects.append(self.Board(
                name=item['name'],
                platform=self.get_type(),
                user=user,
                data=item,
            ))
        self.Board.objects.bulk_create(objects)
        return objects

    def _load_lists(self, boards):
        objects = []
        for board in boards:
            response = self._get_groups_from_platform(board)
            items = json.loads(response.content)
            for item in items['lists']:
                objects.append(self.Group(
                    name=item['name'],
                    board=board,
                    data=item,
                ))
        self.Group.objects.bulk_create(objects)
        return objects

    def _load_cards(self, groups):
        objects = []
        for group in groups:
            response = self._get_cards_from_platform(group)
            items = json.loads(response.content)
            for item in items:
                objects.append(self.Card(
                    name=item['name'],
                    group=group,
                    data=item,
                ))
        self.Card.objects.bulk_create(objects)
        return objects

    def _get_boards_from_platform(self):
        raise NotImplementedError

    def _get_groups_from_platform(self, board):
        raise NotImplementedError

    def _get_cards_from_platform(self, group):
        raise NotImplementedError
