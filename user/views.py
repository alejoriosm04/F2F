from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import UserRegistrationForm

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.backend = 'user.authentication.EmailAuthBackend'
            login(request, user)  # Log the user in after registering
            return redirect('home')  # Redirect to a home page or other appropriate page
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})