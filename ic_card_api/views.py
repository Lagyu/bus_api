import codecs
import csv
from collections import Iterable

from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import QuerySet
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic import ListView
from django.http import HttpResponse, StreamingHttpResponse

from rest_framework import viewsets
from ic_card_api import serializers
from ic_card_api import models
import datetime
import pytz


# Create your views here.


class OfficeBrunchViewSet(viewsets.ModelViewSet):
    queryset = models.OfficeBrunch.objects.all()
    serializer_class = serializers.OfficeBrunchSerializer


class BusRouteViewSet(viewsets.ModelViewSet):
    queryset = models.BusRoute.objects.all()
    serializer_class = serializers.BusRouteSerializer


class BusPlanViewSet(viewsets.ModelViewSet):
    queryset = models.BusPlan.objects.all()
    serializer_class = serializers.BusPlanSerializer


class DeviceViewSet(viewsets.ModelViewSet):
    queryset = models.Device.objects.all()
    serializer_class = serializers.DeviceSerializer


class RideViewSet(viewsets.ModelViewSet):
    queryset = models.Ride.objects.all()
    serializer_class = serializers.RideSerializer


class SuperuserRequiredMixin(object):
    @method_decorator(user_passes_test(lambda u: u.is_authenticated and u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super(SuperuserRequiredMixin, self).dispatch(*args, **kwargs)


class RouteCSVExport(SuperuserRequiredMixin, ListView):
    model = models.BusRoute
    context_object_name = "bus_routes"
    template_name = "ic_card_api/csv_export.html"


class Echo(object):
    @staticmethod
    def write(value):
        """Write the value by returning it, instead of storing in a buffer."""
        return value


def iter_csv(field_names, query_set, pseudo_buffer):
    yield pseudo_buffer.write(codecs.BOM_UTF8)
    writer = csv.writer(pseudo_buffer)
    yield writer.writerow(field_names)
    for item in query_set:
        yield writer.writerow([item.device.bus_route.name,
                               item.member_id,
                               str(item.created_at.astimezone(pytz.timezone('Asia/Tokyo')))])


@user_passes_test(lambda u: u.is_authenticated and u.is_superuser, login_url="/admin/login/")
def download_csv(request):
    start_date_str = request.POST["start_date"]  # type: str
    end_date_str = request.POST["end_date"]  # type: str
    bus_route_list = list(map(lambda x: int(x), request.POST.getlist("checks[]")))  # type: Iterable

    start_datetime = datetime.datetime(year=int(start_date_str.split("-")[0]),
                                       month=int(start_date_str.split("-")[1]),
                                       day=int(start_date_str.split("-")[2]),
                                       hour=0,
                                       minute=0,
                                       second=0,
                                       tzinfo=pytz.timezone('Asia/Tokyo')
                                       )

    end_datetime = datetime.datetime(year=int(end_date_str.split("-")[0]),
                                     month=int(end_date_str.split("-")[1]),
                                     day=int(end_date_str.split("-")[2]),
                                     hour=0,
                                     minute=0,
                                     second=0,
                                     tzinfo=pytz.timezone('Asia/Tokyo')
                                     )

    result_rides = models.Ride.objects.order_by("created_at") \
        .filter(device__bus_route__in=bus_route_list,
                created_at__gt=start_datetime,
                created_at__lt=end_datetime)  # type: QuerySet

    meta = models.Ride._meta
    field_names = ["bus_route".encode("utf-8-sig").decode("utf-8"), "card_id", "created_at"]

    response = StreamingHttpResponse(iter_csv(field_names=field_names, query_set=result_rides, pseudo_buffer=Echo()),
                                     content_type="text/csv")

    response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)

    return response
