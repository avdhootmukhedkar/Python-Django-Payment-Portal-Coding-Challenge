from dj_rest_auth.jwt_auth import get_refresh_view
from dj_rest_auth.registration.views import (
    ConfirmEmailView,
    RegisterView,
    VerifyEmailView,
)
from dj_rest_auth.views import (
    LoginView,
    LogoutView,
    PasswordChangeView,
    PasswordResetConfirmView,
    PasswordResetView,
    UserDetailsView,
)
from django.urls import path, re_path
from rest_framework_simplejwt.views import TokenVerifyView

# app_name = "users"

urlpatterns = [
    path("account-confirm-email/<str:key>/", ConfirmEmailView.as_view()),
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("token/refresh/", get_refresh_view().as_view(), name="token_refresh"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("user/", UserDetailsView.as_view(), name="profile"),
    path("password-reset/", PasswordResetView.as_view()),
    path(
        "password-reset-confirm/<slug:uidb64>/<slug:token>/",
        PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "password/change/",
        PasswordChangeView.as_view(),
        name="password_change",
    ),
    path("verify-email/", VerifyEmailView.as_view(), name="rest_verify_email"),
    path("account-confirm-email/", VerifyEmailView.as_view(), name="account_email_verification_sent"),
    re_path(r"^account-confirm-email/(?P<key>[-:\w]+)/$", VerifyEmailView.as_view(), name="account_confirm_email"),
]
