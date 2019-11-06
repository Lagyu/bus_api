from django.db import models
from django.utils import timezone

import datetime

# Create your models here.


class OfficeBrunch(models.Model):
    name = models.CharField(max_length=100)


class RaspberryPi(models.Model):
    office_brunch = models.ForeignKey(OfficeBrunch, on_delete=models.CASCADE, related_name="raspberry_pis")
    name = models.CharField(max_length=100)

    def get_active_beacons(self):
        beacon_records_within_five_minutes = self.beaconrecord_set.filter(
            detection_time__range=(timezone.now() - datetime.timedelta(minutes=5),
                                   timezone.now()))

        beacons_id_list = []
        beacon_record_count = []
        for beacon_record in beacon_records_within_five_minutes:  # type: BeaconRecord
            if beacon_record.beacon.id not in beacons_id_list:
                beacons_id_list.append(beacon_record.beacon.id)
                beacon_record_count.append(1)
            else:
                beacon_record_count[beacons_id_list.index(beacon_record.beacon.id)] += 1

        active_beacon_ids_list = [beacon_id for beacon_id in beacons_id_list
                                  if beacon_record_count[beacons_id_list.index(beacon_id)] >= 10]

        active_beacons_set = Beacon.objects.filter(pk__in=active_beacon_ids_list)
        return active_beacons_set


class Beacon(models.Model):
    mac_address = models.CharField(max_length=17)

    def is_active(self):
        records = self.beaconrecord_set
        records_in_five_minutes = records.filter(detection_time__range=(timezone.now() - datetime.timedelta(minutes=5),
                                                                        timezone.now()))
        if records_in_five_minutes.count > 10:
            return True
        else:
            return False


class BeaconRecord(models.Model):
    detection_time = models.DateTimeField(auto_now=True)
    beacon = models.ForeignKey(Beacon, on_delete=models.CASCADE)
    raspberry_pi = models.ForeignKey(RaspberryPi, on_delete=models.CASCADE)
    strength = models.IntegerField()


