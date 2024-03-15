from django.urls import path
from .views import generate_recipe_view
#/recipe/generate_recipe/
app_name = 'recipe' 

urlpatterns = [
    path('generate_recipe/', generate_recipe_view, name='generate_recipe_view'),
]