from django.shortcuts import render

from django.shortcuts import render, redirect
from .models import Ingredient

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

