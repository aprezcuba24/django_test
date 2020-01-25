from unittest.mock import patch
from django.test import TestCase
from app.core.ioc_container import TrelloPlatform


class LoadTest(TestCase):

    def test_all(self):
        with patch.object(TrelloPlatform, 'login', return_value=None) as mock_login:
            response = self.client.get('/users/oauth/trello', follow=True)
            url, status = response.redirect_chain[0]
            assert url == '/'
            assert status == 302

        assert mock_login.call_count == 1
