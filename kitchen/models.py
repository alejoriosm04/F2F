from django.db import models
from django.conf import settings

from recipe.models import Recipe

class Ingredient(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1)

class RecipeHadIngredient(models.Model):
    recipe_id = models.ForeignKey(Recipe, on_delete=models.DO_NOTHING)
    ingredient_name = models.CharField(max_length=100)
