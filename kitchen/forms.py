from django import forms
from .models import Ingredient

class RecipeForm(forms.Form):
  details = forms.CharField(
    widget=forms.TextInput(attrs={'placeholder': 'I want a recipe that is …'}),
    max_length=100,
    required=False,
  )
  preference = forms.CharField(
    widget=forms.TextInput(attrs={'placeholder': 'What kind of cuisine do you like?'}),
    max_length=100,
    required=False,
  )


class IngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = ['name']
