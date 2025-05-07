from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import UpdateView
from .models import Profile
from .forms import ProfileForm

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileForm
    template_name = 'user_management/profile_form.html'
    context_object_name = 'profile'

    def get_object(self, queryset=None):
        return Profile.objects.get(user=self.request.user)

