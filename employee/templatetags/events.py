from django.contrib.admin.models import LogEntry
from django import template
register = template.Library()


@register.inclusion_tag('partials/_events.html')
def events():
    logs = LogEntry.objects.select_related().all().order_by('-action_time')[:10]
    return {'events': logs}