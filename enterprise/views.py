import datetime

from django.db.models import Count
from django.utils.functional import cached_property
from django.views.generic import TemplateView, DetailView

from enterprise.models import Employee, Organisation
from equipment.models import Equipment
from reports.models import XLS, PDF


class DashboardMixin(object):

    @cached_property
    def employees(self):
        selection = Employee.all()
        return {
            'count': selection.count()
        }

    @cached_property
    def equipments(self):
        selection = Equipment.all()
        return {
            'count': selection.count()
        }

    def page(self):
        return {
            'title': 'Инвентаризация оборудования'
        }


class Dashboard(TemplateView, DashboardMixin):
    template_name = 'employee/employees.html'


class OrganisationDetailMixin(object):

    @cached_property
    def employees(self):
        employees = self.object.employee_set.select_related('location', 'department')
        return {
            'selection': employees.annotate(equipments_count=Count('equipment')),
            'count': employees.count()
        }

    def page(self):
        title = 'Рабочие места'
        return {
            'title': title
        }


class OrganisationDetailView(DetailView, OrganisationDetailMixin):
    model = Organisation
    template_name = 'employee/list.html'
    context_object_name = 'organisation'

    def get(self, request, *args, **kwargs):
        if 'xls' in request.GET:
            self.object = self.get_object()
            return self.render_to_xls()

        return super(OrganisationDetailView, self).get(request, *args, **kwargs)

    def render_to_xls(self):
        columns = (
            {'repr': '# РМ', 'property': 'id', 'size': 2000},
            {'repr': 'Сотрудник', 'property': 'short_full_name', 'size': 5000},
            {'repr': 'Должность', 'property': 'get_position_display', 'size': 9000},
            {'repr': 'Подразделение', 'property': 'department', 'size': 9000},
            {'repr': 'Расположение', 'property': 'location', 'size': 4000},
            {'repr': 'Кол-во оборудования', 'property': 'equipment_set.count', 'size': 5000}
        )
        xls = XLS(sheet_name='Рабочие места')
        xls.sheet_header = 'Рабочие места: {0}'.format(self.object.title)

        return xls.render(queryset=self.object.employee_set.all(), columns=columns)


class EmployeeDetailMixin(object):

    @cached_property
    def equipments(self):
        selection = self.object.equipment_set.select_related('type')
        return {
            'selection': selection.all(),
            'count': selection.count()
        }

    def page(self):
        title = 'Рабочее место: {0}'.format(self.object.info())
        return {
            'title': title
        }


class EmployeeDetailView(DetailView, EmployeeDetailMixin):
    model = Employee
    template_name = 'employee/detail.html'
    context_object_name = 'employee'

    def get(self, request, *args, **kwargs):
        if 'pdf' in request.GET:
            self.object = self.get_object()
            return self.generate_pdf()

        return super(EmployeeDetailView, self).get(request, *args, **kwargs)

    def generate_pdf(self):
        pdf = PDF(fileName='document')
        pdf.insertRow('Форма учета инвентаризационного оборудования', 'h1')
        pdf.insertRow('от {0}'.format(datetime.datetime.now().strftime('%Y-%m-%d')), 'dt')
        pdf.insertRow(self.object.organisation.title)
        pdf.insertRow('{0} {1}'.format(self.object.get_position_display(), self.object.short_full_name()))
        pdf.insertRow('Список оборудования:', 'h3')

        columns = ('Инв. №', 'Серийный номер', 'Тип', 'Модель')
        queryset = self.object.equipment_set.select_related('type')
        set = [(e.inventory_number, e.serial_number, e.type.value, e.model) for e in queryset]

        pdf.insertTable(columns=columns, queryset=set)
        pdf.insertBreak()
        pdf.insertRow('Всего по списку: {0} ед.'.format(len(set)))
        pdf.insertRow(
            '{0} _______________________________________________________ {1}'.
            format(datetime.datetime.now().strftime('%Y.%m.%d'), self.object.short_full_name()),
            'center',
            lineBreak=False
        )
        pdf.insertRow('(подпись)', 'center_md')

        return pdf.render()
