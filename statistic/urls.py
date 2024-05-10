from django.urls import path
from .views import overview, generate_recommendation

urlpatterns = [
    path('overview/', overview, name='statistics_overview'),
    path('generate-recommendation/', generate_recommendation, name='generate-recommendation'),
]
