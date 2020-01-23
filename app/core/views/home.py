from django.views import View
from django.http import HttpResponse
from app.core.ioc_container import Container
from app.core.models import PlatformType


class HomeView(View):
    def get(self, request):
        Container.get_platforms()
        trello = Container.get_platform(PlatformType.TRELLO)
        return HttpResponse(trello.get_oaut_url())
