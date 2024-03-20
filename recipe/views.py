from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .openAPIadapter import OpenAIAdapter
from kitchen.models import Ingredient
from .models import Recipe
import os

def generate_recipe(user, preference):
    user_ingredients = list(Ingredient.objects.filter(user=user).values_list('name', flat=True))

    if not user_ingredients:
        return JsonResponse({"error": "No ingredients found for the user."}, status=404)

    user_ingredients = ', '.join(user_ingredients)
    adapter = OpenAIAdapter()

    try:
        recipe_data = adapter.generate_response_sync(user_ingredients, preference)

        if not recipe_data:
            # Si la API no devolvió datos, regresa un error
            return JsonResponse({"error": "The OpenAI API did not generate a recipe."}, status=500)

        try:
            # Intenta extraer el título y la receta según el formato esperado
            parts = recipe_data.split('Recipe:')
            if len(parts) < 2 or not parts[0] or not parts[1]:
                raise ValueError("Incomplete recipe format.")

            title = parts[0].replace('Title:', '').strip()
            recipe = parts[1].strip()

            if not title or not recipe:
                raise ValueError("Incomplete recipe format.")

            # Si todo es correcto, guarda la receta en la base de datos
            new_recipe = Recipe(
                user=user,
                title=title,
                description=recipe,
                parameters=user_ingredients,
            )
            new_recipe.save()

            return JsonResponse({
                "title": title,
                "recipe": recipe
            })

        except ValueError as e:
            # Maneja el error de formato en la respuesta
            return JsonResponse({"error": str(e)}, status=500)

    except Exception as e:
        print(e)
        return JsonResponse({"error": "An error occurred while fetching the recipe."}, status=500)
