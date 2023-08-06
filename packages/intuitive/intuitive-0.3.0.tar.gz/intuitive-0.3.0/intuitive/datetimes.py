import datetime

from dateutil.parser import parse
from dateutil.relativedelta import relativedelta

CODES = {
    'day': '%d',
    'month': '%m',
    'month_name': '%B',
    'month_name_short': '%b',
    'year': '%Y',
    'hour': '%H',  # 24-hour clock
    'hour_12': '%I',  # 12-hour clock
    'minute': '%M',
    'second': '%S',
}


def parse_date_string(s, year_first=False):
    try:
        return parse(s, yearfirst=year_first).date()
    except OverflowError:
        return None


def string_to_datetime(datetime_string, date_format):
    date_format = convert_format(date_format)
    return datetime.datetime.strptime(datetime_string, date_format)


def string_to_date(date_string, date_format):
    date_format = convert_format(date_format)
    return datetime.datetime.strptime(date_string, date_format).date()


def date_to_string(date, string_format):
    string_format = convert_format(string_format)
    return datetime.date.strftime(date, string_format)


def datetime_to_string(date_time, string_format):
    string_format = convert_format(string_format)
    return datetime.datetime.strftime(date_time, string_format)


def convert_format(date_format: str) -> str:
    for simple_code, code in CODES.items():
        if simple_code in date_format:
            date_format = date_format.replace(simple_code, code)
    return date_format


def timestamp_to_date(timestamp):
    return timestamp_to_datetime(timestamp).date()


def timestamp_to_datetime(timestamp):
    return datetime.datetime.fromtimestamp(timestamp)


def datetime_to_timestamp(date_time):
    return datetime.datetime.timestamp(date_time)


def date_to_datetime(date, min_time=True):
    if min_time:
        return datetime.datetime.combine(date, datetime.datetime.min.time())
    else:
        return datetime.datetime.combine(date, datetime.datetime.max.time())


def date_generator(start, end, interval=1):
    while start <= end:
        yield start
        start += interval


def reverse_date_generator(end, start, interval=1):
    while end >= start:
        yield end
        end -= interval


def month_generator(start, end, interval=1):
    while start <= end:
        yield start
        start += relativedelta(months=+interval)


def reverse_month_generator(end, start, interval=1):
    while end >= start:
        yield end
        end += relativedelta(months=-interval)
