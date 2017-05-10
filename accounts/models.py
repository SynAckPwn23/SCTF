from django.contrib.auth import get_user_model
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save

User = get_user_model()


class Team(models.Model):
    name = models.CharField(max_length=256)
    users = models.ManyToManyField(User, through='accounts.userprofile')

    @property
    def solved_challenges(self):
        from challenges.models import Challenge
        return Challenge.objects.filter(solved_by__profile__team=self).distinct()

    @property
    def total_points(self):
        return self.solved_challenges.total_points() or 0

    @property
    def position(self):
        return sorted(Team.objects.all(), key=lambda t: -t.total_points).index(self) + 1

    @property
    def num_users(self):
        return self.users.count()

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    team = models.ForeignKey('accounts.Team', null=True)
    user = models.OneToOneField(User, related_name='profile')

    def __str__(self):
        return '{}, Team: {}'.format(self.user.username, self.team)

    @property
    def total_points(self):
        return self.user.solved_challenges.total_points() or 0

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