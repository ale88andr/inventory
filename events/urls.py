from django.conf.urls import url
from events.views import EventListView

urlpatterns = (
    url(r'^$', EventListView.as_view(), name='index'),
)