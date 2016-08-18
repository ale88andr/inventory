from django import forms


class ReportsForm(forms.Form):

    REPORT_TYPES = (
        ('summary', 'Сводный отчёт'),
        # ('by_types', 'По типам оборудования'),
    )

    report_type = forms.ChoiceField(
        label='Тип отчёта',
        choices=REPORT_TYPES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )