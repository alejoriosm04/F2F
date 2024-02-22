from django import forms
from .models import Ingredient

class RecipeForm(forms.Form):
  details = forms.CharField(
    max_length=100,
    help_text="What should the recipe be like?")

class IngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = ['name', 'quantity', 'unit']
