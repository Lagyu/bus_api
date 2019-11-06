from django.shortcuts import render
from django.views.generic import ListView

from bus_api.models import OfficeBrunch, RaspberryPi, Beacon, BeaconRecord
# Create your views here.


class HomeView(ListView):
    model = OfficeBrunch
    context_object_name = "office_brunches"
    template_name = "bus_display/home.html"




