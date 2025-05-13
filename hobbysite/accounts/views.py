"""This file contains the views for the accounts app."""
from django.shortcuts import render, redirect
from .forms import RegisterForm
from user_management.models import Profile


def register_view(request):
    """Handle user registration."""
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(
                user=user,
                display_name=form.cleaned_data['display_name'],
                email=form.cleaned_data['email']
            )
            return redirect('/accounts/login/')
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})
