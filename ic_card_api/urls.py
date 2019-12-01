from django.urls import include, path
from rest_framework import routers
from ic_card_api import views

app_name = "ic_card_api"

router = routers.DefaultRouter()

router.register("ride_record", views.RideViewSet)
router.register("device", views.DeviceViewSet)

router.register("office_brunch", views.OfficeBrunchViewSet)
router.register("bus_route", views.BusRouteViewSet)
router.register("bus_plan", views.BusPlanViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path("csv_export/", views.RouteCSVExport.as_view(), name="csv_export"),
    path("csv_export/download",views.download_csv, name="csv_download")
]
