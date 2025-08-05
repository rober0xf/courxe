import uuid

from django.conf import settings
from django.db import models


# Create your models here.
class Email(models.Model):
    email = models.EmailField(unique=True)
    active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects: models.Manager = models.Manager()


class EmailVerification(models.Model):
    parent = models.ForeignKey(Email, on_delete=models.SET_NULL, null=True)
    email = models.EmailField()
    token = models.UUIDField(default=uuid.uuid1)
    attempts = models.IntegerField(default=0)
    expired = models.BooleanField(default=False)
    last_attempt_at = models.DateTimeField(auto_now=False, auto_now_add=False, blank=True, null=True)
    expired_at = models.DateTimeField(auto_now=False, auto_now_add=False, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects: models.Manager = models.Manager()

    def get_link(self):
        return f"{settings.BASE_URL}/verify/{self.token}"
