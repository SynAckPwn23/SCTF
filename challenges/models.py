from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=256)


class Challenge(models.Model):
    name = models.CharField(max_length=256)
    category = models.ForeignKey('challenges.Category')
    description = models.TextField()
    key = models.CharField(max_length=256)
    points = models.IntegerField()


class Hint(models.Model):
    challenge = models.ForeignKey('challenges.Challenge')
    text = models.TextField


class Attachment(models.Model):
    challenge = models.ForeignKey('challenges.Challenge')
    description = models.TextField()
    file = models.FileField(upload_to='challenges')
