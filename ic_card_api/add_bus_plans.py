import os
import sys
import datetime

import django
import pandas
import pytz

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "../../")
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bus_count.settings')
django.setup()

from ic_card_api import models

csv_df = pandas.read_csv(r"./bus_plans.csv")
for index, row in csv_df.iterrows():
    from_office = models.OfficeBrunch.objects.get(name=row["from"])
    to_office = models.OfficeBrunch.objects.get(name=row["to"])
    bus_route, created = models.BusRoute.objects.get_or_create(from_office_brunch=from_office,
                                                               to_office_brunch=to_office)
    result = models.BusPlan.objects.get_or_create(
        bus_route=bus_route,
        depart_at=pytz.timezone('Asia/Tokyo').localize(datetime.datetime(year=datetime.datetime.now().year,
                                                                         month=datetime.datetime.now().month,
                                                                         day=datetime.datetime.now().day,
                                                                         hour=row["hour_d"],
                                                                         minute=row["minute_d"],
                                                                         second=row["second_d"]
                                                                         )),
        arrive_at=pytz.timezone('Asia/Tokyo').localize(datetime.datetime(year=datetime.datetime.now().year,
                                                                         month=datetime.datetime.now().month,
                                                                         day=datetime.datetime.now().day,
                                                                         hour=row["hour_a"],
                                                                         minute=row["minute_a"],
                                                                         second=row["second_a"]
                                                                         )),
    )
    print(result)
