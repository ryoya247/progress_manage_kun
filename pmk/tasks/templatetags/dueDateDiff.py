from django import template

import datetime

register = template.Library()

@register.filter(expects_localtime=True)
def due_date_diff(value):
    today = datetime.datetime.now().date()
    if type(value) == datetime.date:
        diffDate = (value - today).days
        if diffDate > 0:
            return 'あと{}日'.format(diffDate)
        elif diffDate < 0:
            diffDate = diffDate * -1
            return '{}日前'.format(diffDate)
        else:
            return '今日'
