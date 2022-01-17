import os
import uuid
from uuid import uuid4

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _

GENDER_SELECTION = [
    ("M", "Male"),
    ("F", "Female"),
]


@deconstructible
class UploadToPathAndRename(object):
    def __init__(self, path):
        self.sub_path = path

    def __call__(self, instance, filename):
        ext = filename.split(".")[-1]
        # get filename
        # if instance.pk:
        #     filename = '{}.{}'.format(instance.pk, ext)
        # else:
        #     # set filename as random string
        #     filename = '{}.{}'.format(uuid4().hex, ext)
        filename = "{}.{}".format(uuid4().hex, ext)
        # return the whole path to the file
        return os.path.join(self.sub_path, filename)


class CustomUser(AbstractUser):
    # We don't need to define the email attribute because is inherited from AbstractUser
    gender = models.CharField(max_length=20, choices=GENDER_SELECTION)
    phone_number = models.CharField(max_length=30)
    dob = models.DateField(null=True, blank=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    # profile_picture = models.ImageField(upload_to="profile_images/", blank=True)
    profile_picture = models.ImageField(
        upload_to=UploadToPathAndRename(os.path.join("profile_images")), blank=True, null=True
    )

    def __str__(self):
        return "{}".format(self.email)

    def save(self, *args, **kwargs):
        self.username = self.email
        super(CustomUser, self).save(*args, **kwargs)
