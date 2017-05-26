from itertools import count

from autofixture import generators, register, AutoFixture

from challenges.models import Category, Challenge

categories_names = [
    'C1',
    'C2',
    'C3'
]

class CategoryAutoFixture(AutoFixture):
    field_values = {
        'name': generators.ChoicesGenerator(choices=categories_names),
    }


points = count(start=1)

class ChallengeAutoFixture(AutoFixture):
    field_values = {
        'points': generators.CallableGenerator(lambda *args, **kwargs: next(points)),
        'name': generators.LoremWordGenerator()
    }

register(Category, CategoryAutoFixture)
register(Challenge, ChallengeAutoFixture)
