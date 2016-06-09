from django.conf.urls import include, url
from django.contrib import admin
from employee.views import Dashboard

urlpatterns = [
    url(r'^backend/', include(admin.site.urls)),
    url(r'^dashboard/', include('employee.urls')),
    url(r'^equipments/', include('equipment.urls')),
    url(r'^reports/', include('reports.urls')),
    url(r'^$', Dashboard.as_view(), name='dashboard')
]
