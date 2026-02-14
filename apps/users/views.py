# path: apps/users/views.py
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.shortcuts import redirect
from .forms import UserRegisterForm

class RegisterView(CreateView):
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

    def dispatch(self, request, *args, **kwargs):
        # If the user is already authenticated, redirect them to the course list page
        if request.user.is_authenticated:
            return redirect('courses:course_list')
        return super().dispatch(request, *args, **kwargs)