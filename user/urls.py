from django.conf import settings
from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

urlpatterns = [
    # path('login/', auth_views.LoginView.as_view(), {'extra_context': {'debug': settings.DEBUG}}, name='login'),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("register/", views.register, name="register"),
    path("login/", views.CustomLoginView.as_view(), name="login"),
]
