from django import template
from employee.models.organisation import Organisation
register = template.Library()


@register.inclusion_tag('partials/organisations_menu.html')
def organisations_menu():
    menu = Organisation.all().filter(parent=None)
    return {'menu': menu}
