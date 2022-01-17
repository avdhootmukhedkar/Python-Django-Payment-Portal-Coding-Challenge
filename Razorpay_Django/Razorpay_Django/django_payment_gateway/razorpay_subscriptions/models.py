from django.db import models
#import uuid
#from decimal import Decimal
from django.conf import settings
from django.core.exceptions import ValidationError
#from django.db import models
#from django.db.models import Avg, F, Max, Min, Sum
#from django.shortcuts import get_list_or_404, get_object_or_404, render
from django.utils.translation import gettext_lazy as _

class Subscriptions(models.Model):
    subscriptionid = models.CharField(max_length=30, unique = True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="subscription_user")
    status = models.CharField(max_length=20)
    shorturl = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now = True)

    
    def __str__(self):
        return str(self.subscriptionid)