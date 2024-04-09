from django.urls import path
from . import views

app_name = 'recipe'

urlpatterns = [
    path('generate/', views.generate_recipe, name='generate_recipe'),
    path('view/<int:pk>', views.show_recipe, name='show'),
    path('get_image/', views.get_image, name='get_image'),
]
