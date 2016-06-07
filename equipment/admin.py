from django.contrib import admin

from equipment.models import Equipment, EquipmentTypes

admin.site.register([Equipment, EquipmentTypes])
