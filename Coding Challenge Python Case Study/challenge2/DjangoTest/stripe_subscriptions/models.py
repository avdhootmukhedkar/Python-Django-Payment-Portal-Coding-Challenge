from django.contrib.auth.models import User
from django.db import models

# Create your models here.

Status = [
    ("Active", "Active"),  # Subscription is in active state or trial state
    ("Cancelled", "Cancelled"),  # Subscription is cancelled
]


class StripeCustomer(models.Model):
    """Stripe Customer Model/Table for mapping customers with Stripe Subscriptions"""

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="customer"
    )
    stripeCustomerId = models.CharField(max_length=255)
    stripeSubscriptionId = models.CharField(max_length=255)
    status = models.CharField(max_length=200, choices=Status, default="Active")

    def __str__(self):
        return self.user.username
