from operator import or_

import registration.signals
from cities_light.models import Country
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.dispatch import receiver
from django.db.models.signals import post_save
from functools import reduce



User = get_user_model()


class StatsFromChallengesMixin:
    @property
    def total_points(self):
        return self.solved_challenges.total_points()

    @property
    def num_success(self):
        return self.solved_challenges.count() or 0

    @property
    def num_fails(self):
        return self.failed_challenges.count() or 0

    @property
    def num_failed_challenges(self):
        return self.failed_challenges.distinct().count() or 0

    def num_never_tried_challenges(self):
        from challenges.models import Challenge
        return Challenge.objects.count() - self.num_success - self.num_failed_challenges

    @property
    def progress(self):
        from challenges.models import Challenge
        return int(self.solved_challenges.count() / (Challenge.objects.count() or 1) * 100)

    @property
    def position(self):
        return 0


class Team(models.Model, StatsFromChallengesMixin):
    name = models.CharField(max_length=256)
    users = models.ManyToManyField(User, through='accounts.userprofile')
    created_at = models.DateTimeField(auto_now_add=True, editable=False)


    @property
    def num_users(self):
        return self.users.count()

    @property
    def challengesolved_set(self):
        return reduce(or_,
                      (u.challengesolved_set.all() for u in self.users.all()),
                      Team.objects.none())

    @property
    def solved_challenges(self):
        from challenges.models import Challenge
        return Challenge.objects.filter(solved_by__team=self).distinct()

    @property
    def failed_challenges(self):
        from challenges.models import Challenge
        return Challenge.objects\
            .filter(failed_by__profile__team=self)\
            .distinct()\
            .exclude(pk__in=self.solved_challenges.all())

    def __str__(self):
        return self.name


class UserProfileQuerySet(models.QuerySet):
    def annotate_score(self):
        return self.annotate(points=Coalesce(Sum('solved_challenges__points'), 0))

    def ordered(self, *args):
        return self.annotate_score().order_by('-points', '-created_at')


class UserProfile(models.Model, StatsFromChallengesMixin):
    objects = UserProfileQuerySet.as_manager()

    team = models.ForeignKey('accounts.Team', null=True)
    user = models.OneToOneField(User, related_name='profile')
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.FileField(upload_to='accounts/', default='accounts/user.png')
    job = models.CharField(max_length=255)
    gender = models.CharField(max_length=1, choices=(('M', 'Male'), ('F','Female')))
    website = models.CharField(max_length=255, null=True, blank=True)
    country = models.ForeignKey(Country)

    def __str__(self):
        return '{}, Team: {}'.format(self.user.username, self.team)

    """
    @property
    def challengesolved_set(self):
        return self.user.challengesolved_set

    @property
    def solved_challenges(self):
        return self.user.solved_challenges

    @property
    def failed_challenges(self):
        return self.user.failed_challenges\
            .exclude(pk__in=self.solved_challenges.all())
    """

    @property
    def failed_challenges(self):
        return self._all_failed_challenges.exclude(pk__in=self.solved_challenges.all())

    @property
    def position(self):
        users = UserProfile.objects.ordered()
        return next(i for i, u in enumerate(users, 1) if u.pk == self.pk)

    @property
    def total_points(self):
        return getattr(self, 'points', None) or self.solved_challenges.total_points()


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()