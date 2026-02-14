from django.urls import path
from django.contrib.auth import views as auth_views
from .views import RegisterView

app_name = 'users'

urlpatterns = [
    # Use Django's built-in authentication views for login and logout
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='courses:course_list'), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
]