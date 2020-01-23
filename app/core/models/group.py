from django.db import models
from django.contrib.postgres.fields import JSONField
from .board import Board


class Group(models.Model):
    name = models.CharField(max_length=256)
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    data = JSONField(default=dict, blank=True)
