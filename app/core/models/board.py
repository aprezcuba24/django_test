from django.db import models
from django.contrib.postgres.fields import JSONField
from django_enumfield import enum
from .enum import PlatformType


class Manager(models.Manager):
    def get_by_user(self, user):
        return super().get_queryset().filter(
            user=user
        )

class Board(models.Model):

    objects = Manager()

    name = models.CharField(max_length=256)
    platform = enum.EnumField(PlatformType, default=PlatformType.TRELLO)
    data = JSONField(default=dict, blank=True)
    user = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        null=True,
        related_name="boards",
        blank=True
    )
