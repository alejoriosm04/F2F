from django.shortcuts import render

from django.shortcuts import render, redirect
from .models import Ingredient
from .forms import RecipeForm, IngredientForm
from django.shortcuts import render, redirect, get_object_or_404

def index(request):
    if request.method == "POST":
        form = RecipeForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            ingredients = Ingredient.objects.filter(name__contains=cd['details'])
            print(ingredients)
            # TODO: Add the timestamp to the database.
            return render(request, "home.html", {"form": form, "ingredients": ingredients})
    else:
        form = RecipeForm()
    return render(request, "home.html", {"form": form})

# Create your views here.
def list_ingredients(request):
    ingredients = Ingredient.objects.all()
    return render(request, "list_ingredients.html", {"ingredients": ingredients})


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
        ingredient = Ingredient(name=new_name, quantity=new_quantity, unit=new_unit)
        ingredient.save()
        return redirect("/kitchen/")
    else:
        # Si la solicitud es GET, puedes decidir qué hacer aquí. Por ejemplo, mostrar un formulario vacío o redirigir.
        # Para este ejemplo, redirigiremos al usuario a la lista de ingredientes.
        return redirect("/kitchen/")
    
def view_ingredient(request, ingredient_id):
    ingredient = Ingredient.objects.get(id=ingredient_id)
    return render(request, "view_ingredient.html", {"ingredient": ingredient})
    
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

def delete_ingredient(request, ingredient_id):
    ingredient = Ingredient.objects.get(id=ingredient_id)
    ingredient.delete()
    return redirect("/kitchen/")
