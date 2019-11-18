from django.urls import include, path
from rest_framework import routers
from ic_card_api import views

app_name = "ic_card_api"

router = routers.DefaultRouter()

router.register("ride_record", views.RideSerializer)
router.register("office_brunch", views.OfficeBrunchViewSet)
router.register("device", views.DeviceSerializer)

urlpatterns = [
    path('', include(router.urls)),
]
