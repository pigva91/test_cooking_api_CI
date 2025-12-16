import random

import factory

from ..app.schemas import RecipeCreate


class RecipeCreateFactory(factory.Factory):
    class Meta:
        model = RecipeCreate

    title = factory.Faker("sentence", nb_words=4)
    cooking_time = factory.Faker("pyint", min_value=10, max_value=120)
    ingredients = factory.LazyFunction(
        lambda: random.sample(
            ["Ингредиент_1", "Ингредиент_2", "Ингредиент_3"],
            k=random.randint(1, 3),
        )
    )
    description = factory.Faker("paragraph")
