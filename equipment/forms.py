from django import forms
from .models.equipment_types import EquipmentTypes
from employee.models.employee import Employee


class EquipmentSearchForm(forms.Form):

    blank_choice_type = ((None, '--- Выберите тип ---'),)
    blank_choice_responsible = ((None, '--- Ответственный ---'),)

    SORTED_FIELDS = (
        (None, '--- Сортировать по ---'),
        ('id', 'Системный идентификатор'),
        ('model', 'Модель'),
        ('type', 'Тип оборудования'),
        ('revised_at', 'Дата ревизии'),
        ('inventory_number', 'Инвентарный номер'),
        ('serial_number', 'Серийный номер'),
    )

    ON_PAGE = (
        (None, 10),
        (5, '5'),
        (20, '20'),
        (50, '50'),
        (100, '100'),
        (99999, 'Все'),
    )

    employee_choices = [(c.id, c.short_full_name()) for c in Employee.all()]

    filter_type = forms.ChoiceField(
        choices=tuple(EquipmentTypes.all().values_list('id', 'value')) + blank_choice_type,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    filter_responsible = forms.ChoiceField(
        choices=tuple(employee_choices) + blank_choice_responsible,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    sort_by = forms.ChoiceField(
        choices=SORTED_FIELDS,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    on_page = forms.ChoiceField(
        choices=ON_PAGE,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

