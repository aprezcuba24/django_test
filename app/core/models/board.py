from django.db import models
from django.contrib.postgres.fields import JSONField
from django_enumfield import enum
from .enum import PlatformType


class Board(models.Model):
    name = models.CharField(max_length=256)
    platform = enum.EnumField(PlatformType, default=PlatformType.TRELLO)
    data = JSONField(default=dict, blank=True)
