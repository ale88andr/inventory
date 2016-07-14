from django.conf.urls import url

from enterprise.views import Dashboard, EmployeesView, EmployeeView

urlpatterns = (
    url(r'^v1/$', Dashboard.as_view(), name='dashboard'),
    url(r'^(?P<pk>\d+)/employees/$', EmployeesView.as_view(), name='list'),
    url(r'^employee/(?P<employee_pk>\d+)$', EmployeeView.as_view(), name='detail')
)
