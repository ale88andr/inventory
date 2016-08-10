from django import template
from django.utils.functional import cached_property

from equipment.models import Equipment

register = template.Library()


@cached_property
@register.inclusion_tag('partials/_percents.html')
def equipment_percents():
    selection = Equipment.all()
    count_all = selection.count()

    def get_percent(count):
        return '{0:.0f}'.format(count * 100 / count_all)

    return {
        'count_used': get_percent(selection.exclude(is_used=False).count()),
        'no_inventory': get_percent(selection.filter(inventory_number=None).count()),
        'not_used': get_percent(selection.filter(is_used=False).count()),
        'repaired': get_percent(selection.filter(is_repair=True).count()),
        'count_all': count_all
    }
