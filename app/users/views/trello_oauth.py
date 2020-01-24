from django.views import View
from django.shortcuts import render


class TrelloOAuthView(View):
    def get(self, request):
        # I need to create this class because Trello sends the token in this format:
        # http://domain.con#token=XXXXX
        # For this reason, I need to create a javascript code to catch the token.
        return render(request, 'auth/trello.html')
