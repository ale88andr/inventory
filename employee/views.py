# coding=utf-8
import copy
from io import BytesIO

from django.http import HttpResponse
from django.views.generic import TemplateView
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle

from employee.models import Employee, Organisation
from reports.models import XLS


class Dashboard(TemplateView):
    template_name = 'employee/employees.html'
    page_title = 'Инвентаризация техники'
    employees = Employee.objects.all()

    def count_employees(self):
        return len(self.employees)


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
            header_title += ': ' + self.organisation.title

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
        pdfmetrics.registerFont(TTFont('Calibri', 'assets/css/dist/fonts/calibri.ttf'))
        response = HttpResponse(content_type='application/pdf')
        filename = "form_%s.pdf" % self.employee.surname
        response['Content-Disposition'] = 'attachment; filename=%s' % filename
        buffer = BytesIO()
        document = SimpleDocTemplate(
            buffer,
            pagesize=letter,
            rightMargin=40,
            leftMargin=40,
            topMargin=60,
            bottomMargin=18,
        )
        report = []
        styles = getSampleStyleSheet()

        # Styles definition
        header_style = copy.copy(styles['Normal'])
        header_style.fontName = 'Calibri'
        header_style.fontSize = 18
        header_style.alignment = 0
        header_style.spaceAfter = 6

        header = Paragraph("Бланк учета оборудования", header_style)
        report.append(header)
        headings = ('Инв. №', 'Серийный номер', 'Тип', 'Модель', 'М.П.')
        equipments_set = [
            (e.inventory_number, e.serial_number, e.type.value, e.model, '') for e in self.employee_equipments
        ]

        t = Table([headings] + equipments_set)
        t.setStyle(TableStyle(
            [
                ('GRID', (0, 0), (4, -1), 1, colors.lightgrey),
                ('LINEBELOW', (0, 0), (-1, 0), 2, colors.lightgrey),
                ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                ('FONT', (0,0), (4,-1), 'Calibri')
            ]
        ))
        report.append(t)
        document.build(report)
        response.write(buffer.getvalue())
        buffer.close()

        return response
