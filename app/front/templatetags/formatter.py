from datetime import date
from decimal import Decimal
from django import template

register = template.Library()

@register.filter
def formatter(value):
    if type(value) == date:
        return f'{"{:02d}".format(value.day)}/{"{:02d}".format(value.month)}/{"{:04d}".format(value.year)}'
    elif type(value) in [int, float, Decimal]:
        return ("{:,.2f}".format(value).replace(",", "@").replace(".", ",").replace("@", "."))
    elif not value:
        return ""
    return value