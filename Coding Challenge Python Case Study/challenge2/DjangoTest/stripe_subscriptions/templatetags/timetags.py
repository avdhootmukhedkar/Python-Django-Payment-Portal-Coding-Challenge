# timestamp conversion
import datetime

from django import template

register = template.Library()


def print_timestamp(timestamp):
    """Django template tag to convert timestamp to human readable format"""
    try:
        ts = float(timestamp)
    except ValueError:
        return None
    return datetime.datetime.fromtimestamp(ts)


register.filter(print_timestamp)
