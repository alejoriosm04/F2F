from django.urls import path
from . import views

app_name = 'recipe'

urlpatterns = [
    path('get_image/', views.get_image),
]
