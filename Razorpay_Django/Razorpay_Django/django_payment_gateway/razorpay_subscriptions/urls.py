from django.urls import path

from .views import (
    subscribetoplan ,
    cancel_subscription,
)

app_name = "razorpay_subscriptions"
urlpatterns = [
    path("subscribe/<slug:planid>", subscribetoplan.as_view(), name="subscribe"),
    path("cancel/<slug:subscriptionid>", cancel_subscription.as_view(), name="cancel_my_subscription"),
]
