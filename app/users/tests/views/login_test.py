from django.test import TestCase
from app.core.ioc_container import TrelloPlatform


class LoginTest(TestCase):

    def test_all(self):
        response = self.client.get('/users/login/')
        platforms = response.context['platforms']
        assert len(platforms) == 1  # At this moment the oly platfmor is trello
        assert isinstance(platforms[0], TrelloPlatform)
