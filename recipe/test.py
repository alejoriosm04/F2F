from django.contrib.auth.models import User
from django.test import TestCase

from kitchen.models import RecipeHadIngredient

from .models import Recipe


class RecipeModelTests(TestCase):
    def test_can_delete_recipe(self):
        user = User.objects.create(username="johndoe")
        recipe = Recipe.objects.create(user=user)
        RecipeHadIngredient.objects.create(
            recipe_id=recipe, ingredient_name="Test ingredient"
        )
        recipe.delete()
