from django.views import View
from django.http import HttpResponseRedirect
from django.urls import reverse
from app.core.ioc_container import Container


class OAuthView(View):
    def get(self, request, platform_name):
        platform = Container.get_platform(platform_name)
        platform.login(request)
        return HttpResponseRedirect(reverse('home'))
