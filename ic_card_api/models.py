from functools import reduce

from django.db import models
from django.db.models import QuerySet

import bus_api.models
from django.contrib.auth.models import User
import datetime

from typing import Union, List

from django.utils import timezone
import pytz

import uuid


# Create your models here.


class OfficeBrunch(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class BusRoute(models.Model):
    from_office_brunch = models.ForeignKey(to=OfficeBrunch,
                                           on_delete=models.CASCADE,
                                           related_name="from_office")
    to_office_brunch = models.ForeignKey(to=OfficeBrunch,
                                         on_delete=models.CASCADE,
                                         related_name="to_office")
    display = models.BooleanField(default=True)

    def __str__(self):
        if self.display:
            return self.name
        else:
            return self.name + "(disabled on viewer)"

    @property
    def name(self):
        return self.from_office_brunch.name + "→" + self.to_office_brunch.name

    def get_departure_timetable_for_today(self):
        time_table = BusPlan.objects.all().filter(bus_route=self).order_by(
            "depart_at")  # type: Union[QuerySet, List[BusPlan]]
        current_time = timezone.now().astimezone(pytz.timezone('Asia/Tokyo'))
        departure_time_list_for_today = [
            datetime.datetime(year=current_time.year,
                              month=current_time.month,
                              day=current_time.day,
                              hour=time_table_obj.depart_at.astimezone(pytz.timezone('Asia/Tokyo')).hour,
                              minute=time_table_obj.depart_at.astimezone(pytz.timezone('Asia/Tokyo')).minute,
                              second=time_table_obj.depart_at.astimezone(pytz.timezone('Asia/Tokyo')).second,
                              microsecond=time_table_obj.depart_at.astimezone(pytz.timezone('Asia/Tokyo')).microsecond,
                              tzinfo=time_table_obj.depart_at.astimezone(pytz.timezone('Asia/Tokyo')).tzinfo).astimezone(pytz.timezone('Asia/Tokyo')) for
            time_table_obj in time_table]
        return departure_time_list_for_today

    @property
    def current_time(self):
        return timezone.now().astimezone(pytz.timezone('Asia/Tokyo'))

    @staticmethod
    def get_close_count_timetable_for_today(self):
        time_table = BusPlan.objects.all().filter(bus_route=self).order_by(
            "depart_at")  # type: Union[QuerySet, List[BusPlan]]
        current_time = timezone.now().astimezone(pytz.timezone('Asia/Tokyo'))
        default_count_close_time_list_for_today = \
            [datetime.datetime(year=current_time.year,
                               month=current_time.month,
                               day=current_time.day,
                               hour=time_table_obj.depart_at.astimezone(pytz.timezone('Asia/Tokyo')).hour,
                               minute=time_table_obj.depart_at.astimezone(pytz.timezone('Asia/Tokyo')).minute,
                               second=time_table_obj.depart_at.astimezone(pytz.timezone('Asia/Tokyo')).second,
                               microsecond=time_table_obj.depart_at.astimezone(pytz.timezone('Asia/Tokyo')).microsecond,
                               tzinfo=time_table_obj.depart_at.astimezone(pytz.timezone('Asia/Tokyo')).tzinfo).astimezone(pytz.timezone('Asia/Tokyo'))
             + datetime.timedelta(
                minutes=time_table_obj.default_count_close_after_departure_minutes) for time_table_obj in time_table]
        return default_count_close_time_list_for_today

    def next_bus_departure_datetime_for_today(self):
        # todo: 土日対応
        departure_time_list_for_today = self.get_departure_timetable_for_today()
        if len(departure_time_list_for_today) > 0:
            current_time = timezone.now().astimezone(pytz.timezone('Asia/Tokyo'))
            next_departure_time = reduce(lambda best_time, dep_time: dep_time
            if (current_time < dep_time < best_time)
               or (best_time < current_time < dep_time)
            else best_time, departure_time_list_for_today)

            return next_departure_time
        else:
            return None

    @property
    def next_close_count_datetime_for_today(self):
        # todo: 土日対応
        close_count_time_list_for_today = self.get_departure_timetable_for_today()
        if len(close_count_time_list_for_today) > 0:
            current_time = timezone.now().astimezone(pytz.timezone('Asia/Tokyo'))
            next_close_time = reduce(lambda best_time, close_time: close_time
            if (current_time < close_time < best_time)
               or (best_time < current_time < close_time)
            else best_time, close_count_time_list_for_today)

            return next_close_time.astimezone(pytz.timezone('Asia/Tokyo'))
        else:
            return None

    @property
    def last_close_count_datetime_for_today(self):
        # todo: 土日対応
        close_count_time_list_for_today = self.get_departure_timetable_for_today()
        if len(close_count_time_list_for_today) > 0:
            current_time = timezone.now().astimezone(pytz.timezone('Asia/Tokyo'))
            last_close_time = reduce(lambda best_time, close_time: close_time if (close_time < current_time)
                                     else best_time, close_count_time_list_for_today)

            return last_close_time.astimezone(pytz.timezone('Asia/Tokyo'))
        else:
            return None

    @property
    def unique_rider_count_for_the_next_bus(self):
        count_since_datetime = self.last_close_count_datetime_for_today
        if count_since_datetime:
            unique_user_id = []
            rides_for_the_bus_route = Ride.objects.filter(device__bus_route=self, created_at__gt=count_since_datetime)
            for ride in rides_for_the_bus_route:
                if ride.member_id not in unique_user_id:
                    unique_user_id.append(ride.member_id)

            return {"count": len(unique_user_id), "color": get_color_code(len(unique_user_id))}
        else:
            return {"count": 0, "color": get_color_code(0)}


def get_color_code(ride_number):
    if ride_number == 0:
        return "#94E17F"
    if ride_number == 1:
        return "#9DE171"
    if ride_number == 2:
        return "#ACE163"
    if ride_number == 3:
        return "#C0E255"
    if ride_number == 4:
        return "#DAE247"
    if ride_number == 5:
        return "#E3CD39"
    if ride_number == 6:
        return "#E3AA2A"
    if ride_number == 7:
        return "#E4821C"
    if ride_number == 8:
        return "#E4540E"
    else:
        return "#E52100"


class BusPlan(models.Model):
    bus_route = models.ForeignKey(BusRoute, on_delete=models.CASCADE)
    # Times are DateTimeField for TimeField does not support tzinfo.
    depart_at = models.DateTimeField()
    arrive_at = models.DateTimeField()
    default_count_close_after_departure_minutes = models.IntegerField(default=5)

    def __str__(self):
        return self.bus_route.name + " (" + str(self.depart_at) + "発)"
    

class Device(models.Model):
    bus_route = models.ForeignKey(to=BusRoute, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=100)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)

    def __str__(self):
        return self.name + "(" + self.bus_route.name + ")"


class Ride(models.Model):
    device = models.ForeignKey(to=Device, on_delete=models.CASCADE)
    member_id = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.member_id + " at " + str(self.created_at)
