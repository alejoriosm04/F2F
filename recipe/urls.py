from django.urls import path
from .views import generate_recipe_view

app_name = 'recipe' 

urlpatterns = [
    path('generate_recipe/', generate_recipe_view, name='generate_recipe_view'),
]