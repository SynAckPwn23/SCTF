from django.db import models
from django.db.models import Sum
from django.db.models.functions.base import Coalesce

RelatedUserModel = 'accounts.UserProfile'


class Category(models.Model):
    name = models.CharField(max_length=256, unique=True)
    description = models.TextField()

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name


class ChallengeQuerySet(models.QuerySet):

    def total_points(self):
        return self.aggregate(_sum=Coalesce(Sum('points'), 0))['_sum']

    def filter_difficulty(self, difficulty):
        return self.filter(difficulty=difficulty)

    def easy(self):
        return self.filter_difficulty('E')

    def medium(self):
        return self.filter_difficulty('M')

    def hard(self):
        return self.filter_difficulty('H')


class Challenge(models.Model):
    objects = ChallengeQuerySet.as_manager()

    name = models.CharField(max_length=256)
    category = models.ForeignKey('challenges.Category', related_name='challenges')
    description = models.TextField()
    key = models.CharField(max_length=256)
    points = models.IntegerField()
    difficulty = models.CharField(max_length=1, choices=(
        ('E', 'Easy'),
        ('M', 'Medium'),
        ('H', 'Hard')
    ))

    solved_by = models.ManyToManyField(RelatedUserModel,
                                       related_name='solved_challenges',
                                       through='challenges.ChallengeSolved')

    failed_by = models.ManyToManyField(RelatedUserModel,
                                       related_name='_all_failed_challenges',
                                       through='challenges.ChallengeFail')

    @property
    def newest_solved(self):
        return self.challengesolved_set.order_by('-datetime')

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
    file = models.ImageField(upload_to='challenges')

    def __str__(self):
        return self.name


class ChallengeSolved(models.Model):
    user = models.ForeignKey(RelatedUserModel)
    challenge = models.ForeignKey('challenges.Challenge')
    datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'Challenge: {}, User: {}'.format(self.challenge.name, self.user)


class ChallengeFail(models.Model):
    user = models.ForeignKey(RelatedUserModel)
    challenge = models.ForeignKey('challenges.Challenge')
    datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'Challenge: {}, User: {}'.format(self.challenge.name, self.user)
