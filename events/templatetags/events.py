from django.contrib.admin.models import LogEntry
from django import template
register = template.Library()


@register.inclusion_tag('partials/_events.html')
def events():
    logs = LogEntry.objects.select_related('content_type').all().order_by('-action_time')[:5]

    return {
        'events': logs
    }