from django.db import models
import bus_api.models
from django.contrib.auth.models import User

import uuid


# Create your models here.


class OfficeBrunch(models.Model):
    name = models.CharField(max_length=100)


class Device(models.Model):
    from_office_brunch = models.ForeignKey(to=OfficeBrunch, on_delete=models.CASCADE, related_name="from_office_brunch")
    to_office_brunch = models.ForeignKey(to=OfficeBrunch, on_delete=models.CASCADE, related_name="to_office_brunch")
    name = models.CharField(max_length=100)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)


class Ride(models.Model):
    device = models.ForeignKey(to=Device, on_delete=models.CASCADE)
    member_id = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_created=True)





