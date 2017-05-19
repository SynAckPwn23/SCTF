from autofixture import generators, register, AutoFixture

from challenges.models import Category

categories_names = [
    'C1',
    'C2',
    'C3'
]

class CategoryAutoFixture(AutoFixture):
    field_values = {
        'name': generators.ChoicesGenerator(choices=categories_names),
    }

register(Category, CategoryAutoFixture)