from typing_extensions import Required
from django.contrib.auth.models import User
from django.db import models
from setuptools import Require


# Create your models here.

class Statuses(models.IntegerChoices):
        CREATED = 0, ("Created")
        TRIGGERED = 1, ("Triggered")
        ARCHIVED = 2, ("Archived")
        DELETED = 3, ("Deleted")

class Alert(models.Model):

    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)
    price = models.BigIntegerField(blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    status = models.IntegerField(
        choices=Statuses.choices,
        default=Statuses.CREATED,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return str(self.id)
