from django.shortcuts import render
from .openAPIadapter import OpenAIAdapter
from kitchen.models import Ingredient
from .models import Recipe


def generate_recipe(request, user, preference):
    user_ingredients = list(Ingredient.objects.filter(user=user).values_list('name', flat=True))

    if not user_ingredients:
        return render(request, "recipe.html", {"recipe": None, "error_message": "User has no ingredients."})

    user_ingredients = ', '.join(user_ingredients)
    adapter = OpenAIAdapter()

    try:
        recipe_data = adapter.generate_response_sync(user_ingredients, preference)

        if not recipe_data:
            return render(request, "recipe.html", {"recipe": None, "error_message": "The OpenAI API did not generate a recipe."})

        try:
            # Intenta extraer el título y la receta según el formato esperado
            parts = recipe_data.split('Recipe:')
            if len(parts) < 2 or not parts[0] or not parts[1]:
                raise ValueError("Incomplete recipe format.")

            title = parts[0].replace('Title:', '').strip()
            description = parts[1].strip()

            if not title or not description:
                raise ValueError("Incomplete recipe format.")

            # Si todo es correcto, guarda la receta en la base de datos
            new_recipe = Recipe(
                user=user,
                title=title,
                description=description,
                parameters=user_ingredients,
            )
            new_recipe.save()

            # Split steps using the linebreaks ('\n').
            description = description.splitlines()

            return render(request, "recipe.html", {"recipe": {"title": title, "description": description}, "error_message": None})

        except ValueError as _:
            return render(request, "recipe.html", {"recipe": None, "error_message": "Unknown error."})

    except Exception as _:
        return render(request, "recipe.html", {"recipe": None, "error_message": "Unknown error."})
