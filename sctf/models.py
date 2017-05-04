# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class Team(models.Model):
    name = models.CharField(max_length=256)

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    team = models.ForeignKey('sctf.Team')



