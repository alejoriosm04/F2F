from django import forms

class RecipeForm(forms.Form):
  details = forms.CharField(
    max_length=100,
    help_text="What should the recipe be like?")
