from django.contrib import admin

from enterprise.models import (
    Organisation,
    Location,
    Department,
    Employee
)


@admin.register(Employee)
class EmployeeBackend(admin.ModelAdmin):
    search_fields = ['surname', 'position']
    readonly_fields = ('created_at',)
    save_as = True
    list_display = ('__str__', 'location', 'position', 'department', 'organisation')
    list_filter = ('position', 'organisation', 'state')


@admin.register(Organisation)
class OrganisationBackend(admin.ModelAdmin):
    search_fields = ['title', 'short_title']
    list_display = ('title', 'parent')
    empty_value_display = 'Нет'
    list_filter = ('parent', )


@admin.register(Department)
class DepartmentBackend(admin.ModelAdmin):
    list_filter = ('organisation', )
    list_display = ('__str__', 'organisation')


@admin.register(Location)
class LocationBackend(admin.ModelAdmin):
    search_fields = ['emplacement', ]
    list_display = ('emplacement', 'is_active', 'organisation')
    list_filter = ('organisation', 'is_active')
