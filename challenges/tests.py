from django.contrib.auth import get_user_model
from django.test import TestCase

from challenges.models import Category


class ChallengesTest(TestCase):

    def setUp(self):
        self.test_category = Category.objects.create(name='test')
        self.u1, self.u2, self.u3 = (get_user_model().objects.create_user(
            u,
            u + '@u.it',
            'u1u2u3u4'
        ) for u in ('u1', 'u2', 'u3'))

