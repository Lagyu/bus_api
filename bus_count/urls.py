"""bus_count URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
import ic_card_api.views

admin.site.site_header = "バス乗車履歴API 管理画面"
admin.site.site_title = "バス乗車履歴API 管理画面"

urlpatterns = [
    path('admin/', admin.site.urls, name="admin"),
    path("api/", include("ic_card_api.urls", namespace="ic_card_api"), name="ic_card_api_root"),
    path("", RedirectView.as_view(url="api/")),
    path("beacon_api/", include("bus_api.urls", namespace="bus_api")),
    path("csv_export/", ic_card_api.views.RouteCSVExport.as_view(), name="csv_export"),
    path("csv_export/download/", ic_card_api.views.download_csv, name="csv_download"),
]
