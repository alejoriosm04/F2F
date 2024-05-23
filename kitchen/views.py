from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_GET

from recipe.views import generate_recipe

from .forms import IngredientForm, RecipeForm
from .models import Ingredient, UserActivity


def main(request):
    """View for the main page of FridgeToFeast."""
    return render(request, "main.html")


@login_required
@require_GET
def index(request):
    form = RecipeForm()
    show_modal = request.session.pop(
        "show_modal", False
    )  # Extrae y elimina la variable de sesión
    return render(request, "home.html", {"form": form, "show_modal": show_modal})


@login_required
def list_ingredients(request):
    ingredients = Ingredient.objects.filter(user=request.user).order_by("-created_at")
    last_activity_time = get_last_activity_time(request.user)
    return render(
        request,
        "list_ingredients.html",
        {"ingredients": ingredients, "last_activity_time": last_activity_time},
    )


@login_required
def create_ingredient(request):
    if request.method == "POST":
        new_name = request.POST.get("name")
        quantity = request.POST.get("quantity")
        unit = request.POST.get("unit")
        if new_name == "":
            ingredients = Ingredient.objects.all()
            return render(
                request,
                "list_ingredients.html",
                {
                    "ingredients": ingredients,
                    "error": "Title and description is required",
                },
            )
        ingredient = Ingredient(
            name=new_name, user=request.user, quantity=quantity, unit=unit
        )
        ingredient.save()
        UserActivity.objects.create(
            user=request.user, activity_type=f"Added ingredient {ingredient.name}"
        )
        return redirect("/kitchen/")
    else:
        return redirect("/kitchen/")


@login_required
def delete_ingredient(request, ingredient_id):
    ingredient = Ingredient.objects.get(id=ingredient_id)
    UserActivity.objects.create(
        user=request.user, activity_type=f"Deleted ingredient {ingredient.name}"
    )
    ingredient.delete()
    return redirect("/kitchen/")


def get_last_activity_time(user):
    last_activity = (
        UserActivity.objects.filter(user=user).order_by("-activity_time").first()
    )
    return last_activity.activity_time if last_activity else None


from django.utils.decorators import method_decorator
from django.views.generic.edit import UpdateView


@method_decorator(login_required, name="dispatch")
class IngredientEditView(UpdateView):
    model = Ingredient
    template = ["ingredient"]
    fields = ["name", "quantity", "unit"]
    template_name_suffix = "_edit_form"

    def form_valid(self, form):
        # Registrar la actividad antes de guardar los cambios
        UserActivity.objects.create(
            user=self.request.user,
            activity_type=f"Edited ingredient {form.instance.name}",
        )
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("kitchen:list")
