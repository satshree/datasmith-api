import json
import pytz
import random
import string
import calendar
import logging
from datetime import datetime
from django.conf import settings

logger = logging.getLogger('django')


def log_error(error, module, message=None):
    logger.error(
        f"Exception caught from '{module}' | {error} | {message}", exc_info=True)


def decode_request_body(request):
    try:
        return request.body.decode("utf-8")
    except:
        return request


def parse_request_body(request):
    try:
        return json.loads(decode_request_body(request))
    except:
        return request.data


def parse_date(date, format="%Y-%m-%d %I:%M:%S %p"):
    try:
        return date.astimezone(pytz.timezone(settings.TIME_ZONE)).strftime(format)
    except:
        return date


def get_month_range(date: datetime):
    """Datetime range from start to end of given month."""
    return (
        datetime.strptime(
            f"{parse_date(date, format='%Y-%m-%d')} 00:00:00", "%Y-%m-%d %H:%M:%S").astimezone(pytz.timezone(settings.TIME_ZONE)),
        datetime.strptime(
            f"{parse_date(date, format='%Y-%m')}-{calendar.monthrange(date.year, date.month)[1]} 23:59:59.9999", "%Y-%m-%d %H:%M:%S.%f").astimezone(pytz.timezone(settings.TIME_ZONE))
    )


def get_today(date: datetime):
    """Datetime range from start to end of given date."""
    return (
        datetime.strptime(
            f"{parse_date(date, format='%Y-%m-%d')} 00:00:00", "%Y-%m-%d %H:%M:%S").astimezone(pytz.timezone(settings.TIME_ZONE)),
        datetime.strptime(
            f"{parse_date(date, format='%Y-%m-%d')} 23:59:59.9999", "%Y-%m-%d %H:%M:%S.%f").astimezone(pytz.timezone(settings.TIME_ZONE))
    )


def parse_decimal(value, place=3):
    try:
        return float("{:.{}f}".format(float(value), place))
    except:
        return value


def relative_date(date, timestamp=False) -> str:
    """Get relative date."""

    # RETURN IF NOT DATETIME OBJECT
    if not date:
        return date

    # CONVERT FROM TIMESTAMP
    if timestamp:
        date = datetime.fromtimestamp(date).astimezone(
            pytz.timezone(settings.TIME_ZONE))

    # CURRENT DATETIME
    now = datetime.now(tz=pytz.timezone(settings.TIME_ZONE))

    # DIFFERENCE BETWEEN NOW AND GIVEN DATE
    difference = (now - date).days

    if difference < 0:
        return "🤷🏻‍♂️"

    # TODAY
    if difference < 1:
        # TIME DIFFERENCES FOR ONE DAY
        seconds = (now - date).seconds

        # CONVERT
        minute = int(seconds / 60)
        hour = int(seconds / 3600)

        # FOR MINUTES
        if hour < 1:
            if minute < 1:
                return "Few moments ago"

            if minute == 1:
                return "1 minute ago"
            else:
                return f"{minute} minutes ago"

        # FOR HOURS
        elif hour == 1:
            return "1 hour ago"
        else:
            return f"{hour} hours ago"

    # YESTERDAY
    elif difference < 2:
        return "1 day ago"

    # FEW DAYS
    elif difference > 2 and difference < 8:
        return f"{difference} days ago"

    # ONE WEEK
    elif difference > 7 and difference < 14:
        return "1 week ago"

    # FEW WEEKS
    elif difference > 14 and difference < 30:
        return f"{int(difference/7)} weeks ago"

    # ONE MONTH
    elif difference > 30 and difference < 60:
        return f"1 month ago"

    # FEW MONTHS
    elif difference > 30 and difference < 365:
        return f"{int(difference/30)} months ago"

    # ONE YEAR
    elif difference > 364 and difference < 730:
        return "1 year ago"

    # FEW YEARS
    elif difference > 730:
        return f"{int(difference/365)} years ago"

    # FALLBACK
    return f"{difference} days ago"


def break_integrity_error_key_value_pair(error_message):
    """Break the Django Integrity Error message to the Key-Value pair."""

    key, value = str(error_message).split("=")
    key = key.split("(")[-1][:-1]
    value = value.split(")")[0][1:]

    return key, value


def get_random_string(length=15):
    characters = string.ascii_letters + string.digits
    random_string = ''.join(random.choice(characters) for i in range(length))

    return random_string
