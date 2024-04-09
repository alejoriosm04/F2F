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
        new_quantity = request.POST.get("quantity")
        new_unit = request.POST.get("unit")
        if new_name == "" or new_quantity == "":
            ingredients = Ingredient.objects.all()
            return render(
                request, "list_ingredients.html", {"ingredients": ingredients, "error": "Title and description is required"}
            )
        ingredient = Ingredient(name=new_name, quantity=new_quantity, unit=new_unit, user=request.user)
        ingredient.save()
        return redirect("/kitchen/")
    else:
        return redirect("/kitchen/")

@login_required
def view_ingredient(request, ingredient_id):
    ingredient = Ingredient.objects.get(id=ingredient_id)
    return render(request, "view_ingredient.html", {"ingredient": ingredient})

@login_required
def edit_ingredient(request, ingredient_id):
    ingredient = get_object_or_404(Ingredient, id=ingredient_id)
    if request.method == "POST":
        form = IngredientForm(request.POST, instance=ingredient)
        if form.is_valid():
            form.save()
            return redirect("/kitchen/view/" + str(ingredient.id) + "/")
    else:
        form = IngredientForm(instance=ingredient)
    return render(request, "edit_ingredient.html", {"form": form, "ingredient": ingredient})

@login_required
def delete_ingredient(request, ingredient_id):
    ingredient = Ingredient.objects.get(id=ingredient_id)
    ingredient.delete()
    return redirect("/kitchen/")
