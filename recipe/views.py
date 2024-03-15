from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .openAPIadapter import OpenAIAdapter
from kitchen.models import Ingredient
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
        
        # Asume que ya tienes la clave API almacenada de manera segura.
        adapter = OpenAIAdapter()

        instruction = "Create a recipe using the following ingredients:"
        prompt = f"{ingredients_string}"

        # Llamar a la API de OpenAI para generar la receta, asumiendo que el adapter maneja llamadas sincrónicas.
        recipe_text = adapter.generate_response_sync(instruction, prompt)

        if recipe_text:
            return JsonResponse({"recipe": recipe_text})
        else:
            return JsonResponse({"error": "No recipe was generated."}, status=500)
