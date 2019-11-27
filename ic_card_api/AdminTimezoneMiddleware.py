import pytz
from django.utils import timezone
from django.utils.deprecation import MiddlewareMixin


class AdminTimezoneMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.path.startswith('/admin'):
            timezone.activate(pytz.timezone('Asia/Tokyo'))