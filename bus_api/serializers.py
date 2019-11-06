from rest_framework import serializers
import bus_api.models


class OfficeBrunchSerializer(serializers.ModelSerializer):
    class Meta:
        model = bus_api.models.OfficeBrunch
        fields = "__all__"


class RaspberryPiSerializer(serializers.ModelSerializer):
    class Meta:
        model = bus_api.models.RaspberryPi
        fields = "__all__"


class BeaconSerializer(serializers.ModelSerializer):
    office_brunch = OfficeBrunchSerializer()

    class Meta:
        model = bus_api.models.Beacon
        fields = "__all__"


class BeaconRecordSerializer(serializers.ModelSerializer):
    raspberry_pi = RaspberryPiSerializer()

    class Meta:
        model = bus_api.models.BeaconRecord
        fields = "__all__"

