import csv
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views.generic import RedirectView

from django.apps import apps
from django.contrib import admin

from ic_card_api.models import BusRoute


class ExportCsvMixin:
    def export_as_csv(self, request, queryset):
        return HttpResponseRedirect(reverse("ic_card_api:csv_export"))

    export_as_csv.short_description = "CSV出力"


@admin.register(BusRoute)
class BusRouteMixin(admin.ModelAdmin, ExportCsvMixin):
    actions = ["export_as_csv"]


# all other models
models = apps.get_models()

for model in models:
    try:
        admin.site.register(model)
    except admin.sites.AlreadyRegistered:
        pass
