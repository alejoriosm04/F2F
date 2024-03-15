from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .openAPIadapter import OpenAIAdapter
from kitchen.models import Ingredient
from .models import Recipe
import os
@login_required
def generate_recipe_view(request):
    if request.method == "GET":
        user = request.user

        # Obtener los ingredientes del usuario de manera sincrónica.
        user_ingredients = list(Ingredient.objects.filter(user=user).values_list('name', flat=True))

        if not user_ingredients:
            return JsonResponse({"error": "No ingredients found for the user."}, status=404)

        ingredients_string = ', '.join(user_ingredients)
        
        adapter = OpenAIAdapter()
        recipe_text = adapter.generate_response_sync(ingredients_string)

        if recipe_text:
            title = recipe_text.split('Recipe:')[0].replace('Title:', '').strip()
            recipe = recipe_text.split('Recipe:')[1].strip()
            new_recipe = Recipe(
                user=user,
                title=title,
                description=recipe,
                parameters=ingredients_string,  # Guarda los ingredientes usados como parámetros
                # image se deja como nulo
                # favourite_state por defecto es False
            )
            new_recipe.save()
            return JsonResponse({
                "title": title,
                "recipe": recipe
            })
        else:
            return JsonResponse({"error": "No recipe was generated."}, status=500)
