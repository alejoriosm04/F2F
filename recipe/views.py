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

# async def get_user_ingredients(user):
#     # Asegúrate de que la consulta al ORM está correctamente encapsulada
#     ingredients_query = await sync_to_async(list)(Ingredient.objects.filter(user=user).values_list('name', flat=True))
#     return ingredients_query

# # Tu vista asíncrona
# async def generate_recipe_view(request):
#     # Verifica si el usuario está autenticado de manera asíncrona si es necesario
#     if not request.user.is_authenticated:
#         # Si no está autenticado, redirige adecuadamente
#         return HttpResponseRedirect(reverse('login'))
    
#     user = request.user

#     # Obtén los ingredientes del usuario de forma asíncrona
#     user_ingredients = await get_user_ingredients(user)

#     if not user_ingredients:
#         return JsonResponse({"error": "No ingredients found for the user."}, status=404)
#     ingredients_string = ', '.join(user_ingredients)
    
#     api_key = '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'
#     adapter = OpenAIAdapter(api_key)

#     instruction = "Create a recipe using the following ingredients:"
#     prompt = f"{ingredients_string}"

#     # Generar la respuesta de la receta de manera asíncrona
#     recipe_text = await adapter.generate_response(instruction, prompt)

#     if recipe_text:
#         return JsonResponse({"recipe": recipe_text})
#     else:
#         return JsonResponse({"error": "No recipe was generated."}, status=500)



async def generate_recipe_view(request):
    if request.method == "GET":
        # Asumimos que quieres utilizar una lista predeterminada de ingredientes.
        # Ajusta esto para obtener ingredientes reales según tu aplicación.
        default_ingredients = ['tomato', 'cheese', 'basil']
        
        # Convertir la lista de ingredientes a una cadena de texto para el prompt.
        ingredients_string = ', '.join(default_ingredients)

        # Crear una instancia de OpenAIAdapter con tu clave de API.
        adapter = OpenAIAdapter('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')  # Asegúrate de usar una variable de entorno o un método seguro para manejar tu clave de API.
        instruction = "Create a recipe using the following ingredients:"
        prompt = f"{ingredients_string}"

        # Aquí ya no pasamos 'context' ni 'list_ingredients' porque hemos modificado la clase adapter.
        recipe_text = await adapter.generate_response(instruction, prompt)
        
        # Verifica que recipe_text no esté vacío antes de intentar devolverlo.
        if recipe_text:
            return JsonResponse({"recipe": recipe_text})
        else:
            # Si recipe_text está vacío, devuelve un mensaje de error o respuesta predeterminada.
            return JsonResponse({"error": "No recipe was generated."}, status=500)