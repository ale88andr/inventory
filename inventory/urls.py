from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth.views import login, logout

from employee.views import Dashboard

urlpatterns = [
    url(r'^backend/', include(admin.site.urls)),
    url(r'^dashboard/', include('employee.urls')),
    url(r'^equipments/', include('equipment.urls')),
    url(r'^reports/', include('reports.urls')),
    url(r'^$', Dashboard.as_view(), name='dashboard'),

    # Authentication system url's
    url('^', include('django.contrib.auth.urls')),
    url(r'^login$',  login, name='login'),
    url(r'^logout$', logout, name='logout', kwargs={'next_page': '/'}),
]
