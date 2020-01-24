from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.http import HttpResponseRedirect
from django.urls import reverse
from app.core.ioc_container import Container


class LoadView(LoginRequiredMixin, View):
    def get(self, request):
        platform = Container.get_platform(request.user.platform)
        platform.load_all(request.user)
        return HttpResponseRedirect(reverse('home'))
