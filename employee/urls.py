from django.conf.urls import url

from employee.views import Dashboard, EmployeesView

urlpatterns = (
    url(r'^v1/$', Dashboard.as_view(), name='dashboard'),
    url(r'^(?P<pk>\d+)/employees/$', EmployeesView.as_view(), name='employees')
)
