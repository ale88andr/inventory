from django import template
from equipment.models.equipment_types import EquipmentTypes
register = template.Library()


@register.inclusion_tag('equipment/widgets/equipments_types.html')
def equipment_types_widget():
    equipment_types = EquipmentTypes.annotation.all()
    return {'equipment_types': equipment_types}
