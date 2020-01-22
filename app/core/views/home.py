
import json
from django.views import View
from django.http import HttpResponse
import requests


class HomeView(View):
    def get(self, request):
        token = 'a41b54801363d256bea78e8755d17e9691297789ffbe6ca8e2e9ac01babed246'
        key = 'a19f9131e11fcb963ea4e7cacbf0828e'
        board_id = '59d23ede31ea2d047eac485e'
        list_id = '59d23f716e7b0fbac2cdb848'

        # To find all the user's boards.
        result = requests.get(
            f'https://api.trello.com/1/members/me/boards?key={key}&token={token}'
        )
        # result = requests.get('https://api.trello.com/1/members/me/boards?key={yourKey}&token={yourToken}')
        # To get only the name and id.
        # curl https://api.trello.com/1/members/me/boards?fields=name,url&key={apiKey}&token={apiToken}

        # To find the data for a particular board.
        # curl 'https://api.trello.com/1/boards/{idBoard}?key={yourKey}&token={yourToken}'
        result = requests.get(f'https://api.trello.com/1/boards/{board_id}?key={key}&token={token}')

        # To get the board's list.
        result = requests.get(
            f'https://api.trello.com/1/boards/{board_id}/?fields=name&lists=all&list_fields=all&key={key}&token={token}'
        )

        # To get the cars
        result = requests.get(
            f'https://api.trello.com/1/lists/{list_id}/cards/?fields=all&key={key}&token={token}'
        )

        # print(json.loads(result.content))
        print(result.content)
        return HttpResponse(result.content)
