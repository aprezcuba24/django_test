from unittest.mock import patch
from django.test import TestCase
from app.core.ioc_container import TrelloPlatform
from app.users.models import User


class LoadTest(TestCase):
    def setUp(self):
        pass

    def test_redirect_to_login(self):
        response = self.client.get('/load')
        self.assertRedirects(response, '/users/login/?next=/load')

    def test_all(self):
        with patch.object(TrelloPlatform, 'load_all', return_value=None) as mock_load_all:
            user = User.objects.create(
                username='user1'
            )
            self.client.force_login(user)
            response = self.client.get('/load')
            self.assertRedirects(response, '/')

        assert mock_load_all.call_count == 1
        _, args, _ = mock_load_all.mock_calls[0]
        assert args[0].id == user.id
