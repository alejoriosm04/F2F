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
from django.urls import path, include

from kitchen import views as ingredientViews

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', ingredientViews.index, name='home'),
    path('kitchen/', ingredientViews.list_ingredients, name='list_ingredients'),
    path('kitchen/create/', ingredientViews.create_ingredient, name='create_ingredient'),
    path('kitchen/view/<int:ingredient_id>/', ingredientViews.view_ingredient, name='view_ingredient'),
    path('kitchen/edit/<int:ingredient_id>/', ingredientViews.edit_ingredient, name='edit_ingredient'),
    path('kitchen/delete/<int:ingredient_id>/', ingredientViews.delete_ingredient, name='delete_ingredient'),
    path('user/', include('user.urls')),
    path('kitchen/statistics/', include('statistic.urls')),
    path('recipe/', include('recipe.urls')),
]
