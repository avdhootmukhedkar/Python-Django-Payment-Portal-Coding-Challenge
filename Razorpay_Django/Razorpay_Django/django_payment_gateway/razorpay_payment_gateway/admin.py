from django import forms
from django.contrib import admin

from .models import Order, OrderItem


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    model = OrderItem
    list_display = ("order", "product")
    search_fields = ("order__orderid",)


class OrderItemInline(admin.TabularInline):
    model = OrderItem


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    model = Order
    list_display = ("orderid", "user", "payment_status", "created_at", "updated_at")
    search_fields = (
        "orderid",
        "user__email",
        "user__first_name",
        "user__last_name",
        "order_key",
    )

    inlines = [
        OrderItemInline,
    ]


# Register your models here.
