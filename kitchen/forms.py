from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Ingredient

class RecipeForm(forms.Form):
  details = forms.CharField(
    widget=forms.TextInput(attrs={'placeholder': 'E.g. "20 minutes to prepare", "for a celebration", etc.'}),
    max_length=100,
    required=False,
    label="Any specific requests? (preparation time, length, complexity, etc.)",
  )

  def __create_tuples(lst):
      return [(elem, elem) for elem in lst]

  preference = forms.ChoiceField(
    required=False,
    # I got the list from here: https://en.wikipedia.org/wiki/List_of_cuisines
    choices=__create_tuples([
        _("Any kind of cuisine"),
        _("African"),
        _("Caribbean"),
        _("Central American"),
        _("Central European"),
        _("Chinese"),
        _("East Asian"),
        _("Eastern European"),
        _("German"),
        _("Indian"),
        _("North American"),
        _("Northern European"),
        _("Oceanic"),
        _("South American"),
        _("South Asian"),
        _("South Eastern European"),
        _("Southern European"),
        _("Western European"),
    ]),
    label="What kind of cuisine are you looking for?",
  )


class IngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = ['name']
