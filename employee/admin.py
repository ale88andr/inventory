from django.contrib import admin

from employee.models import *

admin.site.register([Organisation, Location, Employee, Department])
