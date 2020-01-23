from django.contrib.auth.models import AbstractUser
from django.db.models import CharField
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.contrib.postgres.fields import JSONField


class User(AbstractUser):

    # First Name and Last Name do not cover name patterns
    # around the globe.
    name = CharField(_("Name of User"), blank=True, max_length=255)
    platform_integration = JSONField(default=dict, blank=True)

    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"username": self.username})
