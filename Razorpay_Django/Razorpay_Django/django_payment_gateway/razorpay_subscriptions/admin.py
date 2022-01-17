from django.contrib import admin
from django.contrib import admin

from .models import Subscriptions

@admin.register(Subscriptions)
class SubscriptionAdmin(admin.ModelAdmin):
    model = Subscriptions
    list_display = ("subscriptionid", "user", "status", "created_at", "updated_at")
    search_fields = (
        "subscriptionid",
        "user__email",
        "user__first_name",
        "user__last_name",
        )

    