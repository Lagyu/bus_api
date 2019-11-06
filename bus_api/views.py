from django.shortcuts import render
from rest_framework import viewsets
from bus_api import serializers
from bus_api import models
# Create your views here.


class OfficeBrunchViewSet(viewsets.ModelViewSet):
    queryset = models.OfficeBrunch.objects.all()
    serializer_class = serializers.OfficeBrunchSerializer


class RaspberryPiViewSet(viewsets.ModelViewSet):
    queryset = models.RaspberryPi.objects.all()
    serializer_class = serializers.RaspberryPiSerializer


class BeaconViewSet(viewsets.ModelViewSet):
    queryset = models.Beacon.objects.all()
    serializer_class = serializers.BeaconSerializer


class BeaconRecordViewSet(viewsets.ModelViewSet):
    queryset = models.BeaconRecord.objects.all()
    serializer_class = serializers.BeaconRecordSerializer
