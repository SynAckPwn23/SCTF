from itertools import count

from autofixture import generators, register, AutoFixture

from challenges.models import Challenge


points = count(start=1)

names = ('challenge {}'.format(i) for i in(count(start=1)))
keys = ('challenge {}'.format(i) for i in(count(start=1)))


class ChallengeAutoFixture(AutoFixture):
    field_values = {
        'points': generators.CallableGenerator(lambda *args, **kwargs: next(points)),
        'name': generators.CallableGenerator(lambda *args, **kwargs: next(names)),
        'key': generators.CallableGenerator(lambda *args, **kwargs: next(keys)),
    }

register(Challenge, ChallengeAutoFixture)
