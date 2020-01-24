from django.contrib.auth import get_user_model, login as django_login


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
