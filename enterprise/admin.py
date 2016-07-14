from django.contrib import admin

from enterprise.models import *

admin.site.register([Organisation, Location, Employee, Department])
