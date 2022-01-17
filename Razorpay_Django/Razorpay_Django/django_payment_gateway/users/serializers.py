from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import LoginSerializer as RestAuthLoginSerializer
from django.contrib.auth.models import Group
from django.db import transaction
from rest_framework import serializers

from users.models import GENDER_SELECTION, CustomUser


class CustomRegisterSerializer(RegisterSerializer):
    gender = serializers.ChoiceField(choices=GENDER_SELECTION)
    phone_number = serializers.CharField(max_length=30)
    dob = serializers.DateField(required=False)
    first_name = serializers.CharField(max_length=30)
    last_name = serializers.CharField(max_length=30)
    profile_picture = serializers.ImageField(required=False)
    username = None
    # Define transaction.atomic to rollback the save operation in case of error
    @transaction.atomic
    def save(self, request):
        user = super().save(request)
        user.gender = self.data.get("gender")
        user.phone_number = self.data.get("phone_number")
        user.first_name = self.data.get("first_name")
        user.last_name = self.data.get("last_name")
        user.dob = self.data.get("dob")
        user.profile_picture = request.FILES.get("profile_picture")
        user.save()
        return user


class CustomUserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = (
            "pk",
            "email",
            "phone_number",
            "gender",
            "first_name",
            "last_name",
            "dob",
            "profile_picture",
            "groups",
        )
        read_only_fields = (
            "pk",
            "email",
            "groups",
        )


class CustomLoginSerializer(RestAuthLoginSerializer):
    # username = None
    pass
