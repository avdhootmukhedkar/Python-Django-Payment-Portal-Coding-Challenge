from django.shortcuts import render
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

from .models import Subscriptions
from .serializers import (
    subscribeSerializer,
    client,
)


class subscribetoplan(CreateAPIView):
    """
    Create subscription (Action after authenticated user clicks on Subscribe button)
    """

    try:
        permission_classes = [IsAuthenticated]
        # queryset = Order.objects.all()
        serializer_class = subscribeSerializer,


        def post(self, request,planid, *args, **kwargs):
            try:
                print("Args",planid)
                Subscription_serializer = subscribeSerializer(data=self.request.data, context={"request": request,"plan_id":planid})
                # print(Order_serializer.is_valid(), Order_serializer)
                # print(Order_serializer)
                if Subscription_serializer.is_valid():
                    _Order = Subscription_serializer.save()
                    response_data = subscribeSerializer(_Order).data
                else:
                    return Response(Subscription_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                return Response(subscribeSerializer(_Order).data, status=status.HTTP_201_CREATED)
                
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

# Create your views here.

class cancel_subscription(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, subscription, user):
        try:
            return Subscriptions.objects.get(subscriptionid=subscription, user=user)
        except Subscriptions.DoesNotExist:
            raise NotFound(detail=None, code=404)

    def post(self, request, subscriptionid, *args, **kwargs):
        try:
            my_subscription = self.get_object(subscriptionid, request.user)
            
            if my_subscription.status == "active" or my_subscription.status == "created":
                # call refunds api
              
                try:
                    resp = client.subscription.cancel(subscriptionid)
                    print("resp",resp)
                    if resp['status']=="cancelled":  # check is refund is initiated
                        my_subscription.status = resp['status']
                        
                except Exception as e:
                    print(e)
                    raise NotAcceptable(detail="Something went wrong contact please contact us ", code=406)
            my_subscription.save()
            return Response({"Order_cancelled": True}, status=status.HTTP_200_OK)

        except ValidationError as e:
            print("cancel_order post validation Exception", e)
            traceback.print_exc()
            return Response({"errors": dict(e).values()}, status=status.HTTP_409_CONFLICT)
        except Exception as e:
            print("cancel_order post validation Exception", e)
            traceback.print_exc()
            return Response({"errors": "Cancel not possible"}, status=status.HTTP_409_CONFLICT)
