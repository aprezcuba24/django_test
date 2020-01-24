from django.contrib.auth.models import AbstractUser
from django.db.models import CharField
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.contrib.postgres.fields import JSONField
from django_enumfield import enum
from app.core.models import PlatformType


class User(AbstractUser):

    # First Name and Last Name do not cover name patterns
    # around the globe.
    name = CharField(_("Name of User"), blank=True, max_length=255)
    platform_integration = JSONField(default=dict, blank=True)
    platform = enum.EnumField(PlatformType, default=PlatformType.TRELLO)

    def get_absolute_url(self):
        return reverse("home")
        # return reverse("users:detail", kwargs={"username": self.username})
