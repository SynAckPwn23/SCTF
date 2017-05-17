from operator import or_

from django.contrib.auth import get_user_model
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from functools import reduce

User = get_user_model()


class StatsFromChallengesMixin:
    @property
    def total_points(self):
        return self.solved_challenges.total_points() or 0

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
        return int(self.solved_challenges.count() / Challenge.objects.count() * 100)

    @property
    def position(self):
        def compare_key(element):
            return (
                -element.total_points,
                getattr(element.challengesolved_set.last(), 'datetime', 0)
            )
        return sorted(type(self).objects.all(), key=compare_key).index(self) + 1


class Team(models.Model, StatsFromChallengesMixin):
    name = models.CharField(max_length=256)
    users = models.ManyToManyField(User, through='accounts.userprofile')
    created_at = models.DateTimeField(auto_now_add=True)

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
        return Challenge.objects.filter(solved_by__profile__team=self).distinct()

    @property
    def failed_challenges(self):
        from challenges.models import Challenge
        return Challenge.objects\
            .filter(failed_by__profile__team=self)\
            .distinct()\
            .exclude(pk__in=self.solved_challenges.all())

    def __str__(self):
        return self.name


class UserProfile(models.Model, StatsFromChallengesMixin):
    team = models.ForeignKey('accounts.Team', null=True)
    user = models.OneToOneField(User, related_name='profile')
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.FileField(upload_to='accounts/')


    def __str__(self):
        return '{}, Team: {}'.format(self.user.username, self.team)

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


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()