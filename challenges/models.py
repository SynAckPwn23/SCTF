from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=256, unique=True)

    def __str__(self):
        return self.name


class Challenge(models.Model):
    name = models.CharField(max_length=256)
    category = models.ForeignKey('challenges.Category', related_name='challenges')
    description = models.TextField()
    key = models.CharField(max_length=256)
    points = models.IntegerField()

    def __str__(self):
        return self.name


class Hint(models.Model):
    challenge = models.ForeignKey('challenges.Challenge')
    text = models.TextField()

    class Meta:
        unique_together = ('challenge', 'text')

    def __str__(self):
        return self.text


class Attachment(models.Model):
    challenge = models.ForeignKey('challenges.Challenge')
    description = models.TextField()
    file = models.FileField(upload_to='challenges')
