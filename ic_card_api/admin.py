from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import reverse

from ic_card_api import models


class ExportCsvMixin:
    def export_as_csv(self, request, queryset):
        return HttpResponseRedirect(reverse("ic_card_api:csv_export"))

    export_as_csv.short_description = "CSV出力"


@admin.register(models.BusRoute)
class BusRouteMixin(admin.ModelAdmin, ExportCsvMixin):
    actions = ["export_as_csv"]


admin.site.register(models.Ride)
admin.site.register(models.OfficeBrunch)
admin.site.register(models.Device)
admin.site.register(models.BusPlan)
