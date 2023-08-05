from datetime import datetime
import pytz
import tzlocal

__doc__ = "Timezone aware dates"

tz = tzlocal.get_localzone()

strftime = datetime.strftime
strptime = datetime.strptime


def mktimezone(location_string):
    'Make a new timezone object from location_string'
    return pytz.timezone(str(location_string))


def current_date():
    'Current timezone aware date'
    return tz.localize(datetime.now()).date()


def current_time():
    'current timezone aware time'
    return tz.localize(datetime.now()).time()


def current_datetime():
    'Current timezone aware datetime'
    return tz.localize(datetime.now())


def local_timezone():
    'Returns a tzinfo object with the local time zone info'
    return tzlocal.get_localzone()


def convert_timezone(datetime_obj, timezone_string):
    """Convert datetime_obj to another timezone. It should be timezone aware"""
    timezone = mktimezone(timezone_string)
    return datetime_obj.astimezone(timezone)


__all__ = ['strptime', 'strftime', 'current_datetime', 'current_date', 'current_time']
__all__ += ['local_timezone', 'convert_timezone', 'mktimezone']


def patch_datetime(module, server_tz):
    'Overrides .now() and .today() datetime methods'

    class DateTime(module):
        @staticmethod
        def now():
            return convert_timezone(module.now(), server_tz)

        @staticmethod
        def today():
            return convert_timezone(module.now(), server_tz)

    return DateTime
