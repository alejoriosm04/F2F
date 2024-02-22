"""
URL configuration for fridgetofeast project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from ingredient import views as ingredientViews

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', ingredientViews.index),
    path('ingredients/', ingredientViews.list_ingredients, name='list_ingredients'),
    path('ingredients/create/', ingredientViews.create_ingredient, name='create_ingredient'),
    path('ingredients/delete/<int:ingredient_id>/', ingredientViews.delete_ingredient, name='delete_ingredient'),
]
