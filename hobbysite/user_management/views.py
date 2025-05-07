from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Profile
from .forms import ProfileForm
from django.contrib.auth.models import User


@login_required
def profile_update_view(request, username):
    """
    View to display and update the user's profile.
    """
    user = get_object_or_404(User, username=username)
    profile = get_object_or_404(Profile, user=user)
    if request.method == 'POST':
        if 'edit' in request.POST:
            form = ProfileForm(instance=profile)
            return render(request, 'profile_form.html', {'form': form, 'profile': profile, 'is_editing': True})
        elif 'save' in request.POST:
            form = ProfileForm(request.POST, instance=profile)
            if form.is_valid():
                form.save()
                return redirect('user_management:profile_update', username=username)
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'profile_form.html', {'form': form, 'profile': profile, 'is_editing': False})