from django import forms

from equipment.models import Equipment
from .models.equipment_types import EquipmentTypes
from enterprise.models.employee import Employee


class EmployeeCollectionChoice():
    employees = [(c.id, c.short_full_name()) for c in Employee.all()]
    employee_choices = tuple(employees) + ((None, '--- Ответственный ---'),)


class EquipmentFilterForm(forms.Form, EmployeeCollectionChoice):
    filter_type = forms.ChoiceField(
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    filter_responsible = forms.ChoiceField(
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    sort_by = forms.ChoiceField(
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    on_page = forms.ChoiceField(
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    def __init__(self, *args, **kwargs):
        super(EquipmentFilterForm, self).__init__(*args, **kwargs)

        on_page = (
            (None, 10), (5, '5'), (20, '20'), (50, '50'), (100, '100'),(99999, 'Все'),
        )

        sort_by = (
            (None, '--- Сортировать по ---'),
            ('id', 'Системный идентификатор'),
            ('model', 'Модель'),
            ('type', 'Тип оборудования'),
            ('revised_at', 'Дата ревизии'),
            ('inventory_number', 'Инвентарный номер'),
            ('serial_number', 'Серийный номер'),
        )

        self.fields['on_page'].choices = on_page
        self.fields['sort_by'].choices = sort_by
        self.fields['filter_responsible'].choices = EmployeeCollectionChoice.employee_choices
        self.fields['filter_type'].choices = tuple(
            EquipmentTypes.all().values_list('id', 'value')
        ) + ((None, '--- Выберите тип ---'),)


class EquipmentSearchForm(forms.Form):

    search = forms.CharField(
        max_length=80,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Модель, серийный или инвентарный номер...'
        })
    )


class EquipmentChownForm(forms.ModelForm):

    responsible = forms.ModelChoiceField(
        queryset=Employee.all(),
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'}),
        empty_label='Выберите ответственного'
    )

    class Meta:
        model = Equipment
        fields = ('responsible', )


class UploadFileForm(forms.Form):
    file = forms.FileField()
