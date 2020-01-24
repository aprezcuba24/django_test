from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.http import HttpResponse


class HomeView(LoginRequiredMixin, View):
    def get(self, request):
        return HttpResponse(str(request.user))
