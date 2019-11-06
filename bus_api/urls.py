from django.urls import include, path
from rest_framework import routers
from bus_api import views

app_name = "bus_api"

router = routers.DefaultRouter()

router.register("beacon_records", views.BeaconRecordViewSet)

router.register('office_brunches', views.OfficeBrunchViewSet)
router.register('raspberry_pis', views.RaspberryPiViewSet)
router.register("beacons", views.BeaconViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
