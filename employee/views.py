import datetime
from django.views.generic import TemplateView

from employee.models import Employee, Organisation
from equipment.models import Equipment
from reports.models import XLS, PDF


class Dashboard(TemplateView):
    template_name = 'employee/employees.html'
    page_title = 'Инвентаризация техники'
    employees = Employee.all().count()
    equiments = Equipment.all().count()

    def count_employees(self):
        return self.employees

    def count_equipments(self):
        return self.equiments


class EmployeesView(TemplateView):
    template_name = 'employee/list.html'
    page_title = 'Рабочие места'
    collection = None
    organisation = None
    organisation_employees = None

    def dispatch(self, request, *args, **kwargs):
        if kwargs.get('pk'):
            self.collection = Employee.all().filter(organisation=kwargs['pk'])
            self.organisation = Organisation.get(kwargs['pk'])
        else:
            self.collection = Employee.all()
            self.organisation = Organisation.get(0)

        self.organisation_employees = self.organisation.employee_set.count()

        return super(EmployeesView, self).dispatch(request, *args)

    def get(self, request, *args, **kwargs):
        if 'xls' in request.GET:
            return self._export_to_xls()
        return super(EmployeesView, self).get(request, *args, **kwargs)

    def _export_to_xls(self):
        header_title = 'Рабочие места'

        if self.organisation:
            header_title += ': {0}'.format(self.organisation.title)

        columns = (
            {'repr': '# РМ', 'property': 'id', 'size': 2000},
            {'repr': 'Сотрудник', 'property': 'short_full_name', 'size': 5000},
            {'repr': 'Должность', 'property': 'get_position_display', 'size': 9000},
            {'repr': 'Подразделение', 'property': 'department', 'size': 9000},
            {'repr': 'Расположение', 'property': 'location', 'size': 4000},
            {'repr': 'Кол-во оборудования', 'property': 'equipment_set.count', 'size': 5000}
        )
        xls = XLS(sheet_name='Рабочие места')
        xls.sheet_header = header_title

        return xls.render(queryset=self.collection, columns=columns)

    def employees(self):
        return self.collection

    def employees_count(self):
        return len(self.collection)

    def employees_organisation(self):
        return self.organisation


class EmployeeView(TemplateView):
    template_name = 'employee/show.html'
    page_title = 'Рабочее место: '

    def get(self, request, *args, **kwargs):
        if kwargs.get('employee_pk'):
            self.employee = Employee.get(kwargs.get('employee_pk'))
            self.page_title += self.employee.info()
            self.employee_equipments = self.employee.equipment_set.all()

        if 'pdf' in request.GET:
            return self.generate_pdf()

        return super(EmployeeView, self).get(request, *args, **kwargs)

    def generate_pdf(self):
        pdf = PDF(fileName='document')
        pdf.insertRow('Форма учета инвентаризационного оборудования', 'h1')
        pdf.insertRow('от {0}'.format(datetime.datetime.now().strftime('%Y-%m-%d')), 'dt')
        pdf.insertRow(self.employee.organisation.title)
        pdf.insertRow('{0} {1}'.format(self.employee.get_position_display(), self.employee.short_full_name()))
        pdf.insertRow('Список оборудования:', 'h3')

        columns = ('Инв. №', 'Серийный номер', 'Тип', 'Модель')
        set = [(e.inventory_number, e.serial_number, e.type.value, e.model) for e in self.employee_equipments]

        pdf.insertTable(columns=columns, queryset=set)
        pdf.insertBreak()
        pdf.insertRow('Всего по списку: {0} ед.'.format(len(set)))
        pdf.insertRow(
            '{0} _______________________________________________________ {1}'.
            format(datetime.datetime.now().strftime('%Y.%m.%d'), self.employee.short_full_name()),
            'center',
            lineBreak=False
        )
        pdf.insertRow('(подпись)', 'center_md')

        return pdf.render()
