from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Sum


class Category(models.Model):
    name = models.CharField(max_length=256, unique=True)

    def __str__(self):
        return self.name


class ChallengeQuerySet(models.QuerySet):

    def total_points(self):
        return self.aggregate(Sum('points'))['points__sum']


class Challenge(models.Model):
    objects = ChallengeQuerySet.as_manager()

    name = models.CharField(max_length=256)
    category = models.ForeignKey('challenges.Category', related_name='challenges')
    description = models.TextField()
    key = models.CharField(max_length=256)
    points = models.IntegerField()

    solved_by = models.ManyToManyField(get_user_model(),
                                       related_name='solved_challenges',
                                       through='challenges.ChallengeSolved')

    def __str__(self):
        return self.name


class Hint(models.Model):
    challenge = models.ForeignKey('challenges.Challenge', related_name='hints')
    text = models.TextField()

    class Meta:
        unique_together = ('challenge', 'text')

    def __str__(self):
        return self.text


class Attachment(models.Model):
    name = models.CharField(max_length=256)
    challenge = models.ForeignKey('challenges.Challenge', related_name='attachments')
    description = models.TextField()
    file = models.FileField(upload_to='challenges')

    def __str__(self):
        return self.name


class ChallengeSolved(models.Model):
    user = models.ForeignKey(get_user_model())
    challenge = models.ForeignKey('challenges.Challenge')
    datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'User: {}, Challange: {}'.format(self.user.username, self.challenge.name)
