# path: apps/users/views.py
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView

from .forms import UserRegisterForm, UserUpdateForm
from .models import User


class RegisterView(CreateView):
    form_class = UserRegisterForm
    template_name = "users/register.html"
    success_url = reverse_lazy("users:login")

    def dispatch(self, request, *args, **kwargs):
        # If the user is already authenticated, redirect them to the course list page
        if request.user.is_authenticated:
            return redirect("courses:course_list")
        return super().dispatch(request, *args, **kwargs)


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = "users/profile.html"
    success_url = reverse_lazy("users:profile")

    def get_object(self, queryset=None):
        """
        Return the user object for the currently logged-in user.
        This ensures that users can only edit their own profile.
        """
        return self.request.user
