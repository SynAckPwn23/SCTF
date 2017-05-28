from operator import or_

from cities_light.models import Country
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Sum
from django.db.models.expressions import RawSQL
from django.db.models.functions import Coalesce
from django.dispatch import receiver
from django.db.models.signals import post_save


User = get_user_model()

SKILLS_SEPARATOR = '$$$'

class StatsFromChallengesMixin:
    @property
    def total_points(self):
        return getattr(self, 'points', None) or self.solved_challenges.total_points()

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
        # TODO check if can annotate it with sql rownumber
        # if not test if using value_list is faster or not
        elements = self.__class__.objects.ordered().values_list('id', flat=True)
        return next(i for i, e in enumerate(elements, 1) if e == self.pk)

    @property
    def score_over_time(self):
        time_points = []
        points = 0
        for solved in self.challengesolved_set.distinct().order_by('datetime'):
            points += solved.challenge.points
            time_points.append([int(solved.datetime.timestamp()) * 1000, points])
        return time_points

    @property
    def percentage_solved_by_category(self):
        from challenges.models import Category
        return {
            c.name: int(self.solved_challenges.filter(category=c).count() /
                        (c.challenges.count() or 1) * 100)
            for c in Category.objects.all()
        }


class TeamQuerySet(models.QuerySet):
    def annotate_score(self):
        query = """
            select sum(c.points) 
            from challenges_challenge c
            where c.id in (
                select s.challenge_id
                from challenges_challengesolved s
                join accounts_userprofile p on p.id = s.user_id
                where p.team_id = accounts_team.id
            )"""
        return self.annotate(points=RawSQL(query, []))

    def ordered(self, *args):
        return self.annotate_score().order_by('-points', '-created_at')


class Team(models.Model, StatsFromChallengesMixin):
    objects = TeamQuerySet.as_manager()

    name = models.CharField(max_length=256)
    users = models.ManyToManyField(User, through='accounts.userprofile')
    created_at = models.DateTimeField(auto_now_add=True, editable=False)


    @property
    def num_users(self):
        return self.users.count()

    @property
    def challengesolved_set(self):
        from challenges.models import ChallengeSolved
        return ChallengeSolved.objects.filter(user__team=self)

    @property
    def solved_challenges(self):
        from challenges.models import Challenge
        return Challenge.objects.filter(solved_by__team=self).distinct()

    @property
    def failed_challenges(self):
        from challenges.models import Challenge
        return Challenge.objects\
            .filter(failed_by__team=self)\
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
    skills = models.TextField(null=True, blank=True)

    def __str__(self):
        return '{}, Team: {}'.format(self.user.username, self.team)

    @property
    def failed_challenges(self):
        return self._all_failed_challenges.exclude(pk__in=self.solved_challenges.all())




@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()