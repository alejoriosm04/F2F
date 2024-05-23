from django.urls import path

from .views import generate_recommendation, overview

urlpatterns = [
    path("overview/", overview, name="statistics_overview"),
    path(
        "generate-recommendation/",
        generate_recommendation,
        name="generate-recommendation",
    ),
]
