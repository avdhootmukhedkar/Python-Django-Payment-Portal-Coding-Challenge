import json
import traceback

import stripe
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from .models import StripeCustomer

# Create your views here.


@login_required
def home(request):
    """Home page for authenticated users with options to subscribe to Aben Premium membership or cancel subscription if already subscribed."""
    try:

        # Retrieve the subscription & product
        stripe.api_key = settings.STRIPE_SECRET_KEY
        stripe_customer = StripeCustomer.objects.get(
            user=request.user, status="Active"
        )  # Get authenticated user's active subscription record

        subscription = stripe.Subscription.retrieve(
            stripe_customer.stripeSubscriptionId
        )  # Get subscription object from Stripe

        product_id = (
            "prod_KqCFnbizJvloma"  # Product ID for Aben Premium membership
        )
        # product_id = subscription.plan.product
        product = stripe.Product.retrieve(product_id)

        # If user is not subscribed to Aben Premium membership, display subscribe button else display unsubscribe button with subscription details

        return render(
            request,
            "home.html",
            {
                "subscription": subscription,
                "product": product,
            },
        )
    except StripeCustomer.DoesNotExist:

        product_id = "prod_KqCFnbizJvloma"
        product = stripe.Product.retrieve(product_id)
        traceback.print_exc()
        # If user is not subscribed to Aben Premium membership, display subscribe button
        return render(
            request, "home.html", {"subscription": None, "product": product}
        )


@csrf_exempt
def stripe_config(request):
    """Return stripe public key for checkout."""
    try:
        if request.method == "GET":
            stripe_config = {"publicKey": settings.STRIPE_PUBLISHABLE_KEY}
            return JsonResponse(stripe_config, safe=True)
    except Exception as e:
        print("stripe_config:", e)
        traceback.print_exc()
        return JsonResponse({"error": str(e)}, status=500)


@csrf_exempt
def create_checkout_session(request):
    """Stripe checkout session for subscribing to Aben Premium membership."""
    try:
        if request.method == "GET":
            domain_url = "http://localhost:8000/"
            stripe.api_key = settings.STRIPE_SECRET_KEY
            try:
                checkout_session = stripe.checkout.Session.create(
                    client_reference_id=request.user.id
                    if request.user.is_authenticated
                    else None,
                    success_url=domain_url
                    + "success?session_id={CHECKOUT_SESSION_ID}",
                    cancel_url=domain_url + "cancel/",
                    payment_method_types=["card"],
                    mode="subscription",
                    line_items=[
                        {
                            "price": settings.STRIPE_PRICE_ID,
                            "quantity": 1,
                        }
                    ],
                    subscription_data={
                        "trial_period_days": 7,  # Free 7 days trial period
                    },
                )
                return JsonResponse({"sessionId": checkout_session["id"]})
            except Exception as e:
                return JsonResponse({"error": str(e)})
    except Exception as e:
        print("checkout exception", e)
        traceback.print_exc()
        return JsonResponse({"error": str(e)}, status=500)


@csrf_exempt
@login_required
def cancel_subscription(request):
    """Cancel Aben Premium membership subscription."""
    try:
        if request.method == "POST":

            stripe.api_key = settings.STRIPE_SECRET_KEY
            data = json.loads(request.body.decode("UTF-8"))
            subscription_id = data.get("subscription_id")

            stripe.api_key = settings.STRIPE_SECRET_KEY
            stripe_customer = StripeCustomer.objects.get(
                user=request.user, status="Active"
            )

            # if subscription_id belongs to authenticated user, cancel subscription else return error
            if subscription_id == stripe_customer.stripeSubscriptionId:
                cancellation = stripe.Subscription.delete(subscription_id)
                stripe_customer = StripeCustomer.objects.get(
                    user=request.user, stripeSubscriptionId=subscription_id
                )
                stripe_customer.status = "Cancelled"
                stripe_customer.save()

                url = request.build_absolute_uri(reverse("subscriptions-home"))
                return JsonResponse(
                    {"message": "Subscription cancelled", "url": url}
                )
            else:
                return JsonResponse({"message": "Invalid subscription id"})

    except Exception as e:
        print("cancel_subscription:", e)
        traceback.print_exc()
        return JsonResponse({"error": "Subscription cancell error"})


@login_required
def success(request):
    """Success page for subscribing to Aben Premium membership."""
    return render(request, "success.html")


@login_required
def cancel(request):
    """Cancel page for cancelling Aben Premium membership subscription."""
    return render(request, "cancel.html")


@csrf_exempt
def stripe_webhook(request):
    """Stripe webhook for subscription status changes."""
    try:
        stripe.api_key = settings.STRIPE_SECRET_KEY
        endpoint_secret = settings.STRIPE_ENDPOINT_SECRET
        payload = request.body
        sig_header = request.META["HTTP_STRIPE_SIGNATURE"]
        event = None

        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, endpoint_secret
            )
        except ValueError as e:
            # Invalid payload
            return HttpResponse(status=400)
        except stripe.error.SignatureVerificationError as e:
            # Invalid signature
            return HttpResponse(status=400)

        # handle the checkout.session.completed event
        if event["type"] == "checkout.session.completed":
            session = event["data"]["object"]

            # Fetch all the required data from session
            client_reference_id = session.get("client_reference_id")
            stripe_customer_id = session.get("customer")
            stripe_subscription_id = session.get("subscription")

            # Get the user and create a new StripeCustomer
            user = User.objects.get(id=client_reference_id)
            StripeCustomer.objects.create(
                user=user,
                stripeCustomerId=stripe_customer_id,
                stripeSubscriptionId=stripe_subscription_id,
                status="Active",
            )
            # print(user.username + " just subscrbed.")

        return HttpResponse(status=200)
    except Exception as e:
        # print("Webhoot exception", e)
        traceback.print_exc()
        return HttpResponse(status=500)
