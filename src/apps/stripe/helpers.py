from django.urls import reverse

from root import settings
from datetime import datetime
import pytz


def get_full_url(view_name):
    url = f"{settings.BASE_URL}{reverse(view_name)}"
    return url


def get_date_time(date_time, in_timestamp=True):
    timezone = pytz.UTC
    if in_timestamp:
        naive_datetime = datetime.fromtimestamp(date_time)
    else:
        naive_datetime = date_time
    return naive_datetime.replace(tzinfo=timezone)
