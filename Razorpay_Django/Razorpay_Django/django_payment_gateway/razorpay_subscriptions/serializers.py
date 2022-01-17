import uuid
from decimal import Decimal

import razorpay
from django.conf import settings
from django.contrib.auth import models
from django.db.models import fields
from django.utils import timezone
from rest_framework import serializers

from .models import Subscriptions

client = razorpay.Client(auth=(settings.RAZORPAY["key_id"], settings.RAZORPAY["key_secret"]))



class subscribeSerializer(serializers.ModelSerializer):
    subscriptionid = serializers.CharField(required=False)
    status = serializers.CharField(required=False)
    short_url = serializers.CharField(required=False)
    def validate(self, data):
        # custom anything validate
        request = self.context.get("request")
        print("request:",request) 
        plan_id = self.context.get("plan_id")
        data["plan_id"]=plan_id
        # check if user is same as current user
        if request.user != data.get("user"):
            raise serializers.ValidationError("Users cannot place order for other user")

        return data

    def create(self, validated_data):
      print("validated data:",validated_data)
      plan_id = validated_data.pop("plan_id")
      data = {
        "plan_id":plan_id,
        "total_count":6,
      }
      response= client.subscription.create(data=data)
      print("response:",response)
      # {'id': 'sub_ILSRZHs2czLYrJ', 'entity': 'subscription', 'plan_id': 'plan_IEONjv3bZmtgIW', 'status': 'created', 'current_start': None, 'current_end': None, 'ended_at': None, 'quantity': 1, 'notes': [], 'charge_at': None, 'start_at': None, 'end_at': None, 'auth_attempts': 0, 'total_count': 6, 'paid_count': 0, 'customer_notify': True, 'created_at': 1636887271, 'expire_by': None, 'short_url': 'https://rzp.io/i/TTV72H1', 'has_scheduled_changes': False, 'change_scheduled_at': None, 'source': 'api', 'remaining_count': 5}
      validated_data["subscriptionid"]=response["id"]
      validated_data["status"]=response["status"]
      validated_data["shorturl"]=response["short_url"]
      subscription = Subscriptions.objects.create(**validated_data)
      return subscription



    class Meta:
        model = Subscriptions
        fields = (
            "subscriptionid",
            "user",
            "status",
            "short_url",
            
        )
        lookup_field = "subscriptionid"
        extra_kwargs = {"url": {"lookup_field": "subscriptionid"}}
