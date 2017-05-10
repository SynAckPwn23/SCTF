from django.contrib.auth import get_user_model
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save

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
    def progress(self):
        from challenges.models import Challenge
        return int(self.solved_challenges.count() / Challenge.objects.count() * 100)


class Team(models.Model, StatsFromChallengesMixin):
    name = models.CharField(max_length=256)
    users = models.ManyToManyField(User, through='accounts.userprofile')
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def num_users(self):
        return self.users.count()

    @property
    def solved_challenges(self):
        from challenges.models import Challenge
        return Challenge.objects.filter(solved_by__profile__team=self).distinct()

    @property
    def failed_challenges(self):
        from challenges.models import Challenge
        return Challenge.objects.filter(failed_by__profile__team=self).distinct()

    @property
    def position(self):
        return sorted(Team.objects.all(), key=lambda t: -t.total_points).index(self) + 1

    def __str__(self):
        return self.name


class UserProfile(models.Model, StatsFromChallengesMixin):
    team = models.ForeignKey('accounts.Team', null=True)
    user = models.OneToOneField(User, related_name='profile')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{}, Team: {}'.format(self.user.username, self.team)

    @property
    def position(self):
        return sorted(UserProfile.objects.all(), key=lambda t: -t.total_points).index(self) + 1


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()