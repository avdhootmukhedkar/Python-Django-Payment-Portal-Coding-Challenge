from django.urls import path

from . import views

urlpatterns = [
    path(
        "", views.home, name="subscriptions-home"
    ),  # url for home page of authenticated user which allows to subscribe to a plan or cancel subscription if already subscribed
    path(
        "create-checkout-session/", views.create_checkout_session
    ),  # url for invoking stripe checkout session to create new subscription
    path(
        "cancel-subscription/", views.cancel_subscription
    ),  # url for cancelling subscription
    path(
        "config/", views.stripe_config
    ),  # url for exposing stripe public key to frontend
    path(
        "success/", views.success
    ),  # url for success page after successful subscription
    path(
        "cancel/", views.cancel
    ),  # url for success page after successful subscription
    path(
        "webhook/", views.stripe_webhook
    ),  # url for stripe webhook to store stripe subscription id in database
]
