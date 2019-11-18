from rest_framework import serializers
import ic_card_api.models


class OfficeBrunchSerializer(serializers.ModelSerializer):
    class Meta:
        model = ic_card_api.models.OfficeBrunch
        fields = "__all__"


class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ic_card_api.models.Device
        fields = "__all__"


class RideSerializer(serializers.ModelSerializer):
    class Meta:
        model = ic_card_api.models.Ride
        fields = "__all__"
