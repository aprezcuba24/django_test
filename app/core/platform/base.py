class BasePlatform:
    API_URL = ''
    def __init__(self, django_login, Board, User, requests, settings):
        self.django_login = django_login
        self.Board = Board
        self.User = User
        self.requests = requests
        self.settings = settings

    def _get_api_url(self, uri, **kwargs):
        params = [f'{item[0]}={item[1]}' for item in kwargs.items()]
        params = '&'.join(params)
        return f'{self.API_URL}{uri}?{params}'

    def get_name(self):
        return self.get_type().label

    def get_type(self):
        raise NotImplementedError

    def get_oaut_url(self):
        raise NotImplementedError

    def login(self, request):
        user = self._find_or_create(request)
        self.django_login(request, user)
        return user

    def _find_or_create(self, request):
        raise NotImplementedError

    def load_all(self, user):
        self.Board.objects.get_by_user(user).delete()
        boards = self._load_boards(user)
        groups = self._load_lists(user, boards)
        self._load_cards(user, groups)

    def _load_boards(self, user):
        raise NotImplementedError

    def _load_lists(self, user, boards):
        raise NotImplementedError

    def _load_cards(self, user, groups):
        raise NotImplementedError
