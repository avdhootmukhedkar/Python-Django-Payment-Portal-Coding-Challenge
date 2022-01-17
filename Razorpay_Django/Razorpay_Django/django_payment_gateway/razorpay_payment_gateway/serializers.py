import uuid
from decimal import Decimal

import razorpay
from django.conf import settings
from django.contrib.auth import models
from django.db.models import fields
from django.utils import timezone
from rest_framework import serializers

from .models import Order, OrderItem

client = razorpay.Client(auth=(settings.RAZORPAY["key_id"], settings.RAZORPAY["key_secret"]))


class OrderItemsSerialzer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = (
            "id",
            "product",
            "price",
            "quantity",
        )
        # fields = '__all__'
        read_only_fields = ("id",)


class checkoutSerializer(serializers.ModelSerializer):
    order_items = OrderItemsSerialzer(many=True, required=False)
    order_key = serializers.CharField(required=False)

    def validate(self, data):
        # custom anything validate
        request = self.context.get("request")

        # check if user is same as current user
        if request.user != data.get("user"):
            raise serializers.ValidationError("Users cannot place order for other user")

        return data

    def create(self, validated_data):
        """Invoked on pressing checkout button"""
        # print(validated_data, type(validated_data))
        order_items_data = None
        if "order_items" in validated_data:
            order_items_data = validated_data.pop("order_items")
            # print(order_items_data)

        total_paid_calculated = 0.0
        if order_items_data:
            for data in order_items_data:
                print("In serializer", int(data["quantity"]))

                if int(data["quantity"]) > 0:
                    total_paid_calculated += int(data["quantity"]) * float(data["price"])
            validated_data["total_paid"] = round(total_paid_calculated, 3)
            print("Total Calculated", validated_data["total_paid"])

        orderid = uuid.uuid4()
        # print(validated_data, type(validated_data), orderid)
        # print("orderid", orderid)
        """
        Call Payment api and get order key here,pass orderid as receipt
        """
        order_amount = int((float(validated_data["total_paid"])) * 100)
        order_currency = "INR"
        order_receipt = str(orderid)
        # notes = {'Shipping address': 'Bommanahalli, Bangalore'}
        razorpay_order = client.order.create(dict(amount=order_amount, currency=order_currency, receipt=order_receipt))
        # validated_data["order_key"] = uuid.uuid4()
        validated_data["order_key"] = razorpay_order["id"]

        validated_data["total_paid"] = str(validated_data["total_paid"])
        print(validated_data, validated_data["total_paid"])
        order = Order.objects.create(orderid=orderid, **validated_data)

        if order_items_data:
            for data in order_items_data:
                if int(data["quantity"]) > 0:
                    OrderItem.objects.create(order=order, **data)

        return order

    class Meta:
        model = Order
        fields = (
            "orderid",
            "user",
            "total_paid",
            "order_key",
            "payment_option",
            "payment_status",
            "order_items",
        )
        lookup_field = "orderid"
        extra_kwargs = {"url": {"lookup_field": "orderid"}}


class MyOrderSerializer(serializers.ModelSerializer):
    """
    Only read and cancel is supported for customer
    """
     
    order_items = OrderItemsSerialzer(many=True, required=False)
    def validate(self, data):
        # custom anything validate
        request = self.context.get("request")

        # check if user is same as current user
        if request.user != data.get("user"):
            raise serializers.ValidationError("Users cannot place order for other user")

        return data

    class Meta:
        model = Order
        fields = (
            "orderid",
            # "user",
            "total_paid",
            "order_key",
            "payment_status",
            "isRefundRequested",
            "isRefundGranted",
            "order_items",
        )
        lookup_field = "orderid"
        extra_kwargs = {"url": {"lookup_field": "orderid"}}