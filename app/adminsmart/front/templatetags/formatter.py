from datetime import date
from django import template

register = template.Library()

@register.filter
def formatter(value):
    print(type(value))
    if type(value) == date:
        return f'{value.day}/{value.month}/{value.year}'
    elif type(value) == float:
        return ("{:.2f}".format(value))
    elif not value:
        return ""
    return value