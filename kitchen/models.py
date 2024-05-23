from django.db import models
from django.conf import settings

from recipe.models import Recipe


class UserActivity(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    activity_type = models.CharField(max_length=100)
    activity_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.activity_type} at {self.activity_time}"


class Ingredient(models.Model):
    UNIT_CHOICES = [
        ("u", "units"),
        ("kg", "kg"),
        ("l", "liters"),
    ]
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1
    )
    quantity = models.PositiveSmallIntegerField(default=1)
    unit = models.CharField(max_length=2, choices=UNIT_CHOICES, default="u")

    @property
    def full_name(self):
        return f"{self.name} ({self.quantity} {self.get_unit_display()})"


class RecipeHadIngredient(models.Model):
    recipe_id = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient_name = models.CharField(max_length=100)
