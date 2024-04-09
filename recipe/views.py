from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .openAPIadapter import OpenAIAdapter
from kitchen.models import Ingredient
from .models import Recipe


def generate_recipe(request, user, preference):
    user_ingredients = list(Ingredient.objects.filter(user=user).values_list('name', flat=True))

    if not user_ingredients:
        return render(request, "recipe.html", {"recipe": None, "error_message": "User has no ingredients."})

    user_ingredients = ', '.join(user_ingredients)
    adapter = OpenAIAdapter()
    recipe = adapter.generate_response_sync(user_ingredients, preference)

    error_message = None

    if recipe is None:
        error_message = "The OpenAI API did not generate a recipe."
    else:
        # Si todo es correcto, guarda la receta en la base de datos
        new_recipe = Recipe(
            user=user,
            title=recipe['title'],
            description=recipe['description'],
            parameters=user_ingredients,
        )
        new_recipe.save()

    return render(request, "recipe.html", {"recipe": recipe, "error_message": error_message})

@login_required
@require_POST
def get_image(request):
    # recipe_description = request.POST.get('recipe_text')
    # if recipe_description:
        adapter = OpenAIAdapter()
        image_url = adapter.generate_image({'title': "Rice with milk", "description": ['Prepare the tomatoes', 'Cut the onions', 'Enjoy']})
        return JsonResponse({'image_url': image_url})

