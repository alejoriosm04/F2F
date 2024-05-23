from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy

from .forms import LoginForm, UserRegistrationForm


class CustomLoginView(LoginView):
    def form_valid(self, form):
        # Llamar al método base primero
        response = super(CustomLoginView, self).form_valid(form)
        # Establecer la variable de sesión para mostrar el modal
        self.request.session["show_modal"] = True
        return response


def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.backend = "user.authentication.EmailAuthBackend"
            login(request, user)  # Log the user in after registering
            return redirect("home")  # Redirect to a home page or other appropriate page
    else:
        form = UserRegistrationForm()
    return render(request, "registration/register.html", {"form": form})
