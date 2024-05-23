from django.urls import path

from . import views

app_name = "kitchen"
urlpatterns = [
    path("", views.list_ingredients, name="list"),
    path("create/", views.create_ingredient, name="create"),
    path("delete/<int:ingredient_id>/", views.delete_ingredient, name="delete"),
    path("edit/<int:pk>/", views.IngredientEditView.as_view(), name="edit"),
]
