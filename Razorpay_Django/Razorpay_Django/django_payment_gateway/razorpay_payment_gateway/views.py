from django.shortcuts import render

# Create your views here.

import traceback
from decimal import Decimal

import razorpay
import requests
from django.conf import settings
from django.core import serializers
from django.core.exceptions import ValidationError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_list_or_404, get_object_or_404, render
from django.views.decorators.csrf import csrf_exempt
from rest_framework import response, status
from rest_framework.decorators import api_view
from rest_framework.exceptions import NotAcceptable, NotFound

# Create your views here.
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Order, OrderItem
from .serializers import (
    MyOrderSerializer,
    OrderItemsSerialzer,
    checkoutSerializer,
    client,
)


class Checkout(CreateAPIView):
    """
    Create order (Action after authenticated user clicks on Checkout button)
    """

    try:
        permission_classes = [IsAuthenticated]
        # queryset = Order.objects.all()
        serializer_class = checkoutSerializer

        def post(self, request, *args, **kwargs):
            try:

                Order_serializer = checkoutSerializer(data=self.request.data, context={"request": request})
                # print(Order_serializer.is_valid(), Order_serializer)
                # print(Order_serializer)
                if Order_serializer.is_valid():
                    _Order = Order_serializer.save()
                    response_data = checkoutSerializer(_Order).data
                else:
                    return Response(Order_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                # return Response(checkoutSerializer(_Order).data, status=status.HTTP_201_CREATED)

                return Response(response_data, status=status.HTTP_201_CREATED)

            except ValidationError as e:
                print("checkout post validation Exception", e)
                traceback.print_exc()
                return Response({"errors": dict(e).values()}, status=status.HTTP_201_CREATED)

            except Exception as e:
                print("checkout post Exception", e)
                traceback.print_exc()
                raise e
                return Response({"errors": "Something went wrong"}, status=status.HTTP_501_NOT_IMPLEMENTED)

    except Exception as e:
        print("checkout Exception", e)
        traceback.print_exc()


class handle_payment_success(APIView):
    def get_object(self, order_key):
        try:
            return Order.objects.get(order_key=order_key)
        except Order.DoesNotExist:
            raise NotFound(detail=None, code=404)

    def post(self, request, *args, **kwargs):
        try:
            res = request.data
            print("res", res)
            """res will be:
            {'razorpay_payment_id': 'pay_G3NivgSZLx7I9e', 
            'razorpay_order_id': 'order_G3NhfSWWh5UfjQ', 
            'razorpay_signature': '76b2accbefde6cd2392b5fbf098ebcbd4cb4ef8b78d62aa5cce553b2014993c0'}
            """

            ord_id = ""
            raz_pay_id = ""
            raz_signature = ""

            # res.keys() will give us list of keys in res
            for key in res.keys():
                if key == "razorpay_order_id":
                    ord_id = res[key]
                elif key == "razorpay_payment_id":
                    raz_pay_id = res[key]
                elif key == "razorpay_signature":
                    raz_signature = res[key]

            order = self.get_object(ord_id)

            data = {
                "razorpay_order_id": ord_id,
                "razorpay_payment_id": raz_pay_id,
                "razorpay_signature": raz_signature,
            }

            check = client.utility.verify_payment_signature(data)

            if check is not None:
                print("Redirect to error url or error page", check)
                # redirect to checkout page with existing order data and razorpay order_id
                return Response({"error": "Something went wrong"})

            # if payment is successful that means check is None then we will turn isPaid=True
            order.payment_status = "Completed"
            order.razorpay_payment_id = raz_pay_id
            order.razorpay_signature = raz_signature
            order.save()

            res_data = {"message": "payment successfully received!"}
            # redirect to success url of fronent app
            return HttpResponseRedirect(redirect_to="https://google.com")
            return Response(res_data)
        except Exception as e:
            print("handle_payment_success Exception", e)
            traceback.print_exc()
            print("Redirect to error url or error page")
            # redirect to checkout page with existing order data and razorpay order_id
            return Response({"error": "Something went wrong"})


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 1
    page_size_query_param = "page_size"
    max_page_size = 2


class MyOrderList(ListAPIView):
    """
    Order list for customer
    """

    try:
        permission_classes = [IsAuthenticated]
        serializer_class = MyOrderSerializer
        pagination_class = StandardResultsSetPagination
        ordering_fields = ["created_at", "updated_at"]

        def get_queryset(self):
            user = self.request.user
            queryset = Order.objects.all()
            if user is not None:
                queryset = queryset.filter(user=user.id)
                return queryset
            else:
                return None

        # def get(self, request, format=None):
        #     my_orders = get_list_or_404(Order, user=request.user)
        #     serializer = MyOrderSerializer(my_orders, many=True)
        #     return Response(serializer.data)

    except Exception as e:
        print("OrderList Exception", e)
        traceback.print_exc()


class MyOrderDetail(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MyOrderSerializer
    """
    View order for customer
    """

    def get_object(self, orderid, user):
        try:
            return Order.objects.get(orderid=orderid, user=user)
        except Order.DoesNotExist:
            raise NotFound(detail=None, code=404)

    def get(self, request, orderid, format=None):
        myorder = self.get_object(orderid, request.user)
        serializer = MyOrderSerializer(myorder)
        return Response(serializer.data)


class cancel_order(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, orderid, user):
        try:
            return Order.objects.get(orderid=orderid, user=user)
        except Order.DoesNotExist:
            raise NotFound(detail=None, code=404)

    def post(self, request, orderid, *args, **kwargs):
        try:
            my_order = self.get_object(orderid, request.user)
            my_order.order_status = "Cancelled"
            my_order.isRefundRequested = True
            if my_order.payment_status == "Completed" and my_order.payment_option == "razorpay":
                # call refunds api
                payment_id = my_order.razorpay_payment_id
                payment_amount = int(float(my_order.total_paid) * 100)
                print(payment_amount)
                try:
                    resp = client.payment.refund(payment_id, payment_amount)
                    # Refund with Extra Parameters
                    # notes = {'key': 'value'}
                    # resp = client.payment.refund(payment_id, payment_amount, notes=notes)
                    if "id" in resp:  # check is refund is initiated
                        my_order.isRefundGranted = True
                        my_order.payment_status = "Returned"
                except Exception as e:
                    print(e)
                    raise NotAcceptable(detail="Something went wrong contact please contact us ", code=406)
            my_order.save()
            return Response({"Order_cancelled": True}, status=status.HTTP_200_OK)

        except ValidationError as e:
            print("cancel_order post validation Exception", e)
            traceback.print_exc()
            return Response({"errors": dict(e).values()}, status=status.HTTP_409_CONFLICT)
        except Exception as e:
            print("cancel_order post validation Exception", e)
            traceback.print_exc()
            return Response({"errors": "Cancel not possible"}, status=status.HTTP_409_CONFLICT)
