#!/usr/bin/env python

from django.conf import settings
settings.configure()

from autofixture import AutoFixture
from challenges.models import Challenge, Category



category_names = ['C1', 'C2']

category_fixture = AutoFixture(Category,
                               field_values={'name': category_names})

categories = category_fixture.create(2)

challenge_fixture = AutoFixture(Challenge)

challenges = challenge_fixture.create(100)
