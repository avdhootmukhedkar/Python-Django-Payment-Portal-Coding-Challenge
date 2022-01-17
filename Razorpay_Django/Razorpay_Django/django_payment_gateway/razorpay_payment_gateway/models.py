from django.db import models
import uuid
from decimal import Decimal
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Avg, F, Max, Min, Sum
from django.shortcuts import get_list_or_404, get_object_or_404, render
from django.utils.translation import gettext_lazy as _


Payment_Status = [("Pending", "Pending"), ("Completed", "Completed"), ("Returned", "Returned")]


class Order(models.Model):
    orderid = models.UUIDField(default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="order_user")
    payment_option = models.CharField(max_length=200, blank=True, default="razorpay")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now = True)

    total_paid = models.DecimalField(max_digits=12, decimal_places=3, null=True, blank=True)  # from payment API
    order_key = models.CharField(max_length=200)  # from payment API
    razorpay_payment_id = models.CharField(max_length=200, null=True, blank=True)  # from payment API
    razorpay_signature = models.CharField(max_length=200, null=True, blank=True)

    isrefundrequested = models.BooleanField(default=False)
    isrefundgranted = models.BooleanField(default=False) # cancellation api
    payment_status = models.CharField(max_length=200, choices=Payment_Status, default="Pending")

    def __str__(self):
        return str(self.orderid)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="order_items", on_delete=models.CASCADE)
    product = models.CharField(max_length=2000)
    price = models.DecimalField(
        verbose_name=_("Selling Price Inclusive of tax"),
        help_text=_("Selling Price must be numeric value greater than 0"),
        error_messages={
            "name": {
                "max_length": _("Selling Price must be numeric value greater than 0"),
            },
        },
        max_digits=12,
        decimal_places=3,
    )
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now = True)

    def __str__(self):
        return str(self.id)
