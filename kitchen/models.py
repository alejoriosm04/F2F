from django.db import models
from django.conf import settings

# Create your models here.
class Ingredient(models.Model):
    name = models.CharField(max_length=100)
    quantity = models.FloatField()
    unit = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1)
