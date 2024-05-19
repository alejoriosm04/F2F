from django.shortcuts import render

from django.shortcuts import render, redirect
from django.urls import reverse
from .models import Ingredient
from .forms import RecipeForm, IngredientForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_GET

from recipe.views import generate_recipe

def main(request):
    """View for the main page of FridgeToFeast."""
    return render(request, 'main.html')

@login_required
@require_GET
def index(request):
    form = RecipeForm()
    show_modal = request.session.pop('show_modal', False)  # Extrae y elimina la variable de sesión
    return render(request, "home.html", {"form": form, "show_modal": show_modal})

@login_required
def list_ingredients(request):
    ingredients = Ingredient.objects.filter(user=request.user).order_by('-created_at')
    return render(request, "list_ingredients.html", {"ingredients": ingredients})

@login_required
def create_ingredient(request):
    if request.method == "POST":
        new_name = request.POST.get("name")
        quantity = request.POST.get("quantity")
        unit = request.POST.get("unit")
        if new_name == "":
            ingredients = Ingredient.objects.all()
            return render(
                request, "list_ingredients.html", {"ingredients": ingredients, "error": "Title and description is required"}
            )
        ingredient = Ingredient(name=new_name, user=request.user, quantity=quantity, unit=unit)
        ingredient.save()
        return redirect("/kitchen/")
    else:
        return redirect("/kitchen/")

@login_required
def delete_ingredient(request, ingredient_id):
    ingredient = Ingredient.objects.get(id=ingredient_id)
    ingredient.delete()
    return redirect("/kitchen/")


from django.utils.decorators import method_decorator
from django.views.generic.edit import UpdateView
@method_decorator(login_required, name="dispatch")
class IngredientEditView(UpdateView):
    model = Ingredient
    template = ["ingredient"]
    fields = ["name", "quantity", "unit"]
    template_name_suffix = "_edit_form"

    def get_success_url(self):
        return reverse("kitchen:list")
