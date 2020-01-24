from django.views import View
from django.shortcuts import render
from app.core.ioc_container import Container


class LoginView(View):
    def get(self, request):
        return render(request, 'auth/login.html', dict(
            platforms=Container.get_platforms()
        ))
