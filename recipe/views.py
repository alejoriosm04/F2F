from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .openAPIadapter import OpenAIAdapter
from kitchen.models import Ingredient, RecipeHadIngredient
from .models import Recipe
from kitchen.forms import RecipeForm

@login_required
@require_POST
def generate_recipe(request):
    form = RecipeForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        user = request.user
        details = cd['details']
        preference = cd['preference']
        portions = cd['portions']
        # TODO: Add the timestamp to the database.

        user_ingredients = list(Ingredient.objects.filter(user=user))
        if not user_ingredients:
            return render(request, "recipe.html", {"recipe": None, "error_message": "User has no ingredients."})

        unchanged_user_ingredients = [i.name for i in user_ingredients]
        user_ingredients = [i.full_name for i in user_ingredients]
        user_ingredients = ', '.join(user_ingredients)
        adapter = OpenAIAdapter()
        recipe = adapter.generate_response_sync(user_ingredients, details, preference, portions)

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
                    cuisine=preference,
                    number_of_portions=portions,
                    )
            new_recipe.save()

            for ingredient in unchanged_user_ingredients:
                new_ingredient = RecipeHadIngredient(
                        recipe_id=new_recipe,
                        ingredient_name=ingredient,
                )
                new_ingredient.save()

            new_recipe.id
            return redirect(new_recipe)

        return render(request, "recipe.html", {"recipe": recipe, "error_message": error_message})

@login_required
def show_recipe(request, pk):
    recipe = Recipe.objects.get(id=pk)
    import ast
    recipe.description = ast.literal_eval(recipe.description) # Deserialize safely.
    return render(request, "recipe.html", {"recipe": recipe, "error_message": None})

@login_required
@require_POST
def get_image(request):
    recipe_id = request.POST.get('recipe_id')
    if recipe_id:
        adapter = OpenAIAdapter()
        image_url = adapter.generate_image(recipe_id)
        return JsonResponse({'image_url': image_url})


from django.utils.decorators import method_decorator
from django.views.generic import ListView
@method_decorator(login_required, name="dispatch")
class RecipeHistoryView(ListView):
    paginate_by = 5
    paginate_orphans = 2
    template_name = "history.html"

    def get_queryset(self):
        return (Recipe.objects.
                filter(user=self.request.user).
                order_by("-generation_date") # Recent recipes first.
        )
