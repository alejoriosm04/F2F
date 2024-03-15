from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from functools import wraps
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import JsonResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from asgiref.sync import sync_to_async
from .openAPIadapter import OpenAIAdapter
import asyncio
from kitchen.models import Ingredient

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
        api_key = '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'
        adapter = OpenAIAdapter(api_key)

        instruction = "Create a recipe using the following ingredients:"
        prompt = f"{ingredients_string}"

        # Llamar a la API de OpenAI para generar la receta, asumiendo que el adapter maneja llamadas sincrónicas.
        recipe_text = adapter.generate_response_sync(instruction, prompt)

        if recipe_text:
            return JsonResponse({"recipe": recipe_text})
        else:
            return JsonResponse({"error": "No recipe was generated."}, status=500)

# async def generate_recipe_view(request):
#     if request.method == "GET":
#         # Asumimos que quieres utilizar una lista predeterminada de ingredientes.
#         # Ajusta esto para obtener ingredientes reales según tu aplicación.
#         default_ingredients = ['tomato', 'cheese', 'basil']

#         # Convertir la lista de ingredientes a una cadena de texto para el prompt.
#         ingredients_string = ', '.join(default_ingredients)

#         # Crear una instancia de OpenAIAdapter con tu clave de API.
#         adapter = OpenAIAdapter('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')  # Asegúrate de usar una variable de entorno o un método seguro para manejar tu clave de API.
#         instruction = "Create a recipe using the following ingredients:"
#         prompt = f"{ingredients_string}"

#         # Aquí ya no pasamos 'context' ni 'list_ingredients' porque hemos modificado la clase adapter.
#         recipe_text = await adapter.generate_response(instruction, prompt)

#         # Verifica que recipe_text no esté vacío antes de intentar devolverlo.
#         if recipe_text:
#             return JsonResponse({"recipe": recipe_text})
#         else:
#             # Si recipe_text está vacío, devuelve un mensaje de error o respuesta predeterminada.
#             return JsonResponse({"error": "No recipe was generated."}, status=500)