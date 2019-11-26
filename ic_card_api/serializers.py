from rest_framework import serializers
import ic_card_api.models


class OfficeBrunchSerializer(serializers.ModelSerializer):
    class Meta:
        model = ic_card_api.models.OfficeBrunch
        fields = "__all__"


class BusPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = ic_card_api.models.BusPlan
        fields = "__all__"


class BusRouteSerializer(serializers.ModelSerializer):
    last_close_count_datetime_for_today = serializers.ReadOnlyField()
    next_close_count_datetime_for_today = serializers.ReadOnlyField()
    unique_rider_count_for_the_next_bus = serializers.ReadOnlyField()
    name = serializers.ReadOnlyField()

    class Meta:
        model = ic_card_api.models.BusRoute
        fields = ["from_office_brunch",
                  "to_office_brunch",
                  "name",
                  "next_close_count_datetime_for_today",
                  "last_close_count_datetime_for_today",
                  "unique_rider_count_for_the_next_bus"
                  ]


class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ic_card_api.models.Device
        fields = "__all__"


class RideSerializer(serializers.ModelSerializer):
    class Meta:
        model = ic_card_api.models.Ride
        fields = "__all__"
