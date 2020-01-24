from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.shortcuts import render
from app.core.models import Board


class HomeView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'pages/home.html', dict(
            boards=Board.objects.get_by_user(request.user),
        ))
