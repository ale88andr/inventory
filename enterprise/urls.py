from django.conf.urls import url

from enterprise.views import Dashboard, EmployeeDetailView, OrganisationDetailView

urlpatterns = (
    url(r'^v1/$', Dashboard.as_view(), name='dashboard'),
    url(r'^(?P<pk>\d+)$', OrganisationDetailView.as_view(), name='detail'),
    url(r'^employee/(?P<pk>\d+)$', EmployeeDetailView.as_view(), name='employee')
)
