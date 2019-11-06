from bus_display import views
from django.urls import path


app_name = "bus_display"

urlpatterns = [
    path("", views.HomeView.as_view(), name="home")
]
