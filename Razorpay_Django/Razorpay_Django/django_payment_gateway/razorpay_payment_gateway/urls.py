from django.urls import path

from .views import (
    Checkout,
    MyOrderDetail,
    MyOrderList,
    cancel_order,
    handle_payment_success,
)

app_name = "razorpay_payment_gateway"
urlpatterns = [
    path("checkout", Checkout.as_view(), name="checkout"),
    path("payment_successful", handle_payment_success.as_view(), name="order_payment_success"),
    path("myorders/", MyOrderList.as_view(), name="my_orders"),
    path("myorders/<slug:orderid>", MyOrderDetail.as_view(), name="my_order_details"),
    path("myorders/cancel/<slug:orderid>", cancel_order.as_view(), name="cancel_my_order"),
]
