from django import template
from django.utils.functional import cached_property
from equipment.models import Equipment

register = template.Library()


@cached_property
@register.assignment_tag(name='counter')
def equipment_counter():
    selection = Equipment.all()
    count_all = selection.count()
    unused = selection.filter(is_used=False).count()

    return {
        'all': count_all,
        'unused': unused,
        'used': count_all - unused,
        'repair': selection.filter(is_repair=True).count(),
        'without_inventory': selection.filter(inventory_number=None).count()
    }
