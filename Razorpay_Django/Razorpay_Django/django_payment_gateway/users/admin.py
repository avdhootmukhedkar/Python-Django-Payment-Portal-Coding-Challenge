from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from .forms import CustomUserChangeForm, CustomUserCreationForm, GroupAdminForm
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm
    model = CustomUser

    list_display = ("email", "first_name", "last_name", "gender", "phone_number")
    # list_filter = ('is_superuser','is_staff')
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal info", {"fields": ("gender", "phone_number", "first_name", "last_name", "dob", "profile_picture")}),
        ("Permissions", {"fields": ("is_superuser", "is_staff", "is_active", "groups", "user_permissions")}),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "gender",
                    "phone_number",
                    "password1",
                    "password2",
                    "first_name",
                    "last_name",
                    "dob",
                    "profile_picture",
                ),
            },
        ),
    )
    search_fields = ("email", "first_name", "last_name")
    ordering = ("email",)
    # filter_horizontal = ()


admin.site.register(CustomUser, CustomUserAdmin)

# Unregister the original Group admin.
admin.site.unregister(Group)

# Create a new Group admin.
class GroupAdmin(admin.ModelAdmin):
    # Use our custom form.
    form = GroupAdminForm
    # Filter permissions horizontal as well.
    filter_horizontal = ["permissions"]


# Register the new Group ModelAdmin.
admin.site.register(Group, GroupAdmin)
