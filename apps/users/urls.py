# path: apps/users/urls.py
from django.contrib.auth import views as auth_views
from django.urls import path, reverse_lazy

from .views import ProfileUpdateView, RegisterView

app_name = "users"

urlpatterns = [
    # Use Django's built-in authentication views for login and logout
    path("login/", auth_views.LoginView.as_view(template_name="users/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(next_page="courses:course_list"), name="logout"),
    path("register/", RegisterView.as_view(), name="register"),
    path("profile/", ProfileUpdateView.as_view(), name="profile"),
    # Password reset view.
    path(
        "password-reset/",
        auth_views.PasswordResetView.as_view(
            template_name="users/password_reset.html",
            email_template_name="users/password_reset_email.html",
            success_url=reverse_lazy("users:password_reset_done"),
        ),
        name="password_reset",
    ),
    # "Email sent" view after requesting a password reset.
    path(
        "password-reset/done/",
        auth_views.PasswordResetDoneView.as_view(template_name="users/password_reset_done.html"),
        name="password_reset_done",
    ),
    # Password reset confirmation view (the link the user clicks in the email).
    path(
        "password-reset-confirm/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="users/password_reset_confirm.html",
            success_url=reverse_lazy("users:password_reset_complete"),
        ),
        name="password_reset_confirm",
    ),
    # Password reset complete view (after successfully resetting the password).
    path(
        "password-reset-complete/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="users/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
]
