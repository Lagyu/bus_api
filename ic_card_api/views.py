from django.shortcuts import render
from rest_framework import viewsets
from ic_card_api import serializers
from ic_card_api import models
# Create your views here.


class OfficeBrunchViewSet(viewsets.ModelViewSet):
    queryset = models.OfficeBrunch.objects.all()
    serializer_class = serializers.OfficeBrunchSerializer


class DeviceSerializer(viewsets.ModelViewSet):
    queryset = models.Device.objects.all()
    serializer_class = serializers.DeviceSerializer


class RideSerializer(viewsets.ModelViewSet):
    queryset = models.Ride.objects.all()
    serializer_class = serializers.RideSerializer
