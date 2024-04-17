from django import forms
from .models import Ingredient

class RecipeForm(forms.Form):
  details = forms.CharField(
    widget=forms.TextInput(attrs={'placeholder': 'E.g. "20 minutes to prepare", "for a celebration", etc.'}),
    max_length=100,
    required=False,
    label="Any specific requests? (preparation time, length, complexity, etc.)",
  )
  preference = forms.CharField(
    widget=forms.TextInput(attrs={'placeholder': 'What kind of cuisine do you like?'}),
    max_length=100,
    required=False,
    label="What kind of cuisine are you looking for?",
  )


class IngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = ['name']
