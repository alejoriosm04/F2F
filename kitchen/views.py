from django.shortcuts import render

from django.shortcuts import render, redirect
from .models import Ingredient
from .forms import RecipeForm, IngredientForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_GET

from recipe.views import generate_recipe

@login_required
@require_GET
def index(request):
    form = RecipeForm()
    return render(request, "home.html", {"form": form})

@login_required
def list_ingredients(request):
    ingredients = Ingredient.objects.filter(user=request.user)
    return render(request, "list_ingredients.html", {"ingredients": ingredients})

@login_required
def create_ingredient(request):
    if request.method == "POST":
        new_name = request.POST.get("name")
        if new_name == "":
            ingredients = Ingredient.objects.all()
            return render(
                request, "list_ingredients.html", {"ingredients": ingredients, "error": "Title and description is required"}
            )
        ingredient = Ingredient(name=new_name, user=request.user)
        ingredient.save()
        return redirect("/kitchen/")
    else:
        return redirect("/kitchen/")

@login_required
def delete_ingredient(request, ingredient_id):
    ingredient = Ingredient.objects.get(id=ingredient_id)
    ingredient.delete()
    return redirect("/kitchen/")
