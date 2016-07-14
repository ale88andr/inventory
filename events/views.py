from django.contrib.admin.models import LogEntry
from django.views.generic import ListView


class EventListView(ListView):
    model = LogEntry
    template_name = 'events/index.html'
    page_title = 'События системы'
