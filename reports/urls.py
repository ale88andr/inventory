from django.conf.urls import url
from .views import ReportsView

urlpatterns = (
    url(r'^$', ReportsView.as_view(), name='reports'),
)
