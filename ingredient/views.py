from django.shortcuts import render

from django.shortcuts import render, redirect
from .models import Ingredient
from .forms import RecipeForm

def index(request):
    if request.method == "POST":
        form = RecipeForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            print(cd)
            # TODO: Add the timestamp to the database.
            return redirect("/")
    else:
        form = RecipeForm()
    return render(request, "home.html", {"form": form})

# Create your views here.
def list_ingredients(request):
    ingredients = Ingredient.objects.all()
    return render(request, "list_ingredients.html", {"ingredients": ingredients})


def create_ingredient(request):
    new_name = request.POST["name"]
    new_quantity = request.POST["quantity"]
    new_unit = request.POST["unit"]
    if new_name == "" or new_quantity == "":
        ingredients = Ingredient.objects.all()
        return render(
            request, "list_ingredients.html", {"ingredients": ingredients, "error": "Title and description is required"}
        )
    ingredient = Ingredient(name=new_name, quantity=new_quantity, unit=new_unit)
    ingredient.save()
    return redirect("/ingredients/")


def delete_ingredient(request, ingredient_id):
    ingredient = Ingredient.objects.get(id=ingredient_id)
    ingredient.delete()
    return redirect("/ingredients/")
