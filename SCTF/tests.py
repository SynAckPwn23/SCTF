from itertools import chain, repeat

from cities_light.models import Country
from django.contrib.auth import get_user_model
from django.test import TestCase

from accounts.models import Team, UserProfile
from challenges.models import Category, Challenge, ChallengeSolved


class UserScoreTest(TestCase):
    def setUp(self):
        test_category = Category.objects.create(name='test')
        country = Country.objects.create(name='Italy')

        # create 9 users: u0, u1, ... u8
        self.users = [get_user_model().objects.create_user(
            'u{}'.format(i),
            'u{}@test.com'.format(i),
            'u1u2u3u4'
        ) for i in range(9)]

        # create 3 teams: t0, t1, t2
        self.teams = [Team.objects.create(
            name='t{}'.format(i), created_by_id=i+1
        ) for i in range(3)]

        # teams - users association: t0: (u0, u1, u2), t1: (u3, u4, u5), t2: (u6, u7, u8)
        teams_users = chain.from_iterable(repeat(t, 3) for t in self.teams)

        # create users profile
        for u in self.users:
            UserProfile.objects.create(user=u, job='job', gender='M', country=country, team=next(teams_users))

        # create 9 challenges: c0, c1, ..., c8
        self.challenges = [
            Challenge.objects.create(name='c{}'.format(i), points=i, category=test_category)
            for i in range(9)
        ]

        # solved challenges: each user u_i solves all challenges from c_0 to c_i (ie: u2 solves c0,c1,c2)
        for i, u in enumerate(self.users, 1):
            for c in self.challenges[:i]:
                ChallengeSolved.objects.create(user=u.profile, challenge=c)


    def test_users_score(self):
        for i, u in enumerate(UserProfile.objects.annotate_score().all(), 1):
            self.assertEqual(u.points, sum(c.points for c in self.challenges[:i]))

    def test_users_score(self):
        for i, u in enumerate(UserProfile.objects.ordered().all(), 1):
            self.assertEqual(u.position, i)

