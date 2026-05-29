"""Template context: timezone, dates, calendar."""

import zoneinfo
from datetime import datetime
from datetime import timezone as dt_timezone

from django.utils import timezone

from shop.services import fetch_exchange_rate
from shop.utils import format_datetime_dd_mm_yyyy, text_calendar


def site_context(request):
    """Inject user timezone, current dates, and FX rate."""
    tz_name = request.session.get('django_timezone', 'Europe/Minsk')
    try:
        user_tz = zoneinfo.ZoneInfo(tz_name)
    except zoneinfo.ZoneInfoNotFoundError:
        user_tz = zoneinfo.ZoneInfo('Europe/Minsk')

    now_utc = timezone.now()
    now_local = timezone.localtime(now_utc, user_tz)

    server_tz = zoneinfo.ZoneInfo(datetime.now().astimezone().tzname())
    server_now = timezone.localtime(now_utc)


    fx = fetch_exchange_rate('BYN', 'USD')

    return {
        'user_timezone': tz_name,
        'current_date_local': now_local.strftime('%d/%m/%Y'),
        'current_datetime_local': format_datetime_dd_mm_yyyy(now_utc, user_tz),
        'current_datetime_utc': format_datetime_dd_mm_yyyy(now_utc, dt_timezone.utc),
        'server_tz': server_tz,
        'server_datetime': format_datetime_dd_mm_yyyy(now_utc, server_tz),
        'text_calendar': text_calendar(now_local.year, now_local.month),
        'fx_rate': fx.get('rate'),
    }
