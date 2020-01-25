from django.test import TestCase
from app.core.models import Board
from app.users.models import User

class HomeTest(TestCase):

    def test_redirect_to_login(self):
        response = self.client.get('/')
        self.assertRedirects(response, '/users/login/?next=/')

    def test_boards_by_user(self):
        user = User.objects.create(
            username='user1'
        )
        other_user = User.objects.create(
            username='other_user',
        )
        Board.objects.bulk_create([
            Board(name='board1', user=user),
            Board(name='board2', user=user),
        ])
        Board.objects.bulk_create([
            Board(name='board3', user=other_user),
        ])

        self.client.force_login(user)
        response = self.client.get('/')
        boards = [board.name for board in response.context['boards']]
        assert len(boards) == 2
        assert 'board1' in boards
        assert 'board2' in boards

        self.client.force_login(other_user)
        response = self.client.get('/')
        boards = [board.name for board in response.context['boards']]
        assert len(boards) == 1
        assert 'board3' in boards
