from django import forms

from equipment.models import Equipment
from .models.equipment_types import EquipmentTypes
from employee.models.employee import Employee


class EmployeeCollectionChoice():

    employees = [(c.id, c.short_full_name()) for c in Employee.all()]
    employee_choices = tuple(employees) + ((None, '--- Ответственный ---'),)


class EquipmentFilterForm(forms.Form, EmployeeCollectionChoice):

    blank_choice_type = ((None, '--- Выберите тип ---'),)

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

    filter_type = forms.ChoiceField(
        choices=tuple(EquipmentTypes.all().values_list('id', 'value')) + blank_choice_type,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    filter_responsible = forms.ChoiceField(
        choices=EmployeeCollectionChoice.employee_choices,
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


class EquipmentSearchForm(forms.Form):

    search = forms.CharField(
        max_length=80,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Модель, серийный или инвентарный номер...'})
    )


class EquipmentChownForm(forms.ModelForm, EmployeeCollectionChoice):

    responsible = forms.ChoiceField(
        choices=EmployeeCollectionChoice.employee_choices,
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Equipment
        fields = ('responsible', )
