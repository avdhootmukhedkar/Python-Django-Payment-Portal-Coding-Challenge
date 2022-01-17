from django.urls import include, path

# app_name = "accounts"
urlpatterns = [
    path(
        "", include("django_registration.backends.one_step.urls")
    ),  # url for registration
    path(
        "", include("django.contrib.auth.urls")
    ),  # url for login, logout, password reset, password change
]
