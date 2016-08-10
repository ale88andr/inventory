from django.contrib import admin
from equipment.models import Equipment, EquipmentTypes


@admin.register(Equipment)
class EquipmentBackend(admin.ModelAdmin):
    empty_value_display = 'Отсутствует'
    fieldsets = (
        ('Основные данные', {
            'fields': ('type', 'model', 'serial_number', 'inventory_number', 'responsible', 'created_at')
        }),
        ('Дополнительно', {
            'classes': ('collapse',),
            'fields': ('revised_at', 'note', ('is_used', 'is_repair')),
        }),
    )
    list_display = ('model', 'type', 'inventory_number', 'is_used', 'responsible', 'revised_at')
    list_filter = ('type', 'responsible', 'model', 'is_used', 'is_repair')
    list_per_page = 25
    list_select_related = ('responsible', 'type')
    readonly_fields = ('created_at',)
    save_as = True
    search_fields = ['model', 'inventory_number', 'serial_number']


@admin.register(EquipmentTypes)
class EquipmentTypesBackend(admin.ModelAdmin):
    search_fields = ['value']


admin.site.site_header = 'Инвентаризация: администрирование сервиса'
