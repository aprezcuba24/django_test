from django.db import models
from django.contrib.postgres.fields import JSONField
from .group import Group


class Card(models.Model):
    name = models.TextField()
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    data = JSONField(default=dict, blank=True)
