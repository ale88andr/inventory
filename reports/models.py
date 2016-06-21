from datetime import date, datetime
import xlwt
from django.db.models import Count
from django.http import HttpResponse
from equipment.models.equipment import Equipment
from equipment.models.equipment_types import EquipmentTypes


class Report:
    encoding = 'utf-8'
    content_type = 'application/vnd.ms-excel'
    sheet_password = '123'

    header_bold = xlwt.easyxf('''
        font: bold on, height 200;
        pattern: pattern solid, fore_colour ice_blue;
        align: horiz center, vert center
    ''')
    header_style = xlwt.easyxf('''
        font: bold on, height 160;
        pattern: pattern solid, fore_colour ice_blue;
        align: horiz center
    ''')
    group_style = xlwt.easyxf('''
        font: bold True;
        pattern: pattern solid, fore_colour ice_blue;
        align: horiz right
    ''')
    group_style_l = xlwt.easyxf('''
        font: bold True;
        pattern: pattern solid, fore_colour ice_blue;
        align: horiz left
    ''')

    def __init__(self, filename, report_name):
        self.get_queryset()
        self.response = HttpResponse(content_type=self.content_type)
        self.response['Content-Disposition'] = 'attachment; filename=%s_%s.xls' % (filename, Report.get_datetime())
        self.report_name = report_name
        self.workbook = xlwt.Workbook(encoding=self.encoding)

    @staticmethod
    def get_datetime():
        return datetime.today().strftime('%Y-%m-%d_%H%M%S')

    def get_queryset(self):
        self.queryset = EquipmentTypes.objects.all().annotate(types_count=Count('equipment'))

    def set_protection(self, sheet):
        if isinstance(sheet, xlwt.Worksheet):
            sheet.protect = True
            sheet.wnd_protect = True
            sheet.obj_protect = True
            sheet.scen_protect = True
            sheet.password = self.sheet_password
        else:
            raise Exception('Can\'t set sheet protection')

        self.workbook.protect = True
        self.workbook.wnd_protect = True
        self.workbook.obj_protect = True

    def summary_report(self):

        sheet = self.workbook.add_sheet(self.report_name, cell_overwrite_ok=True)

        row_num = 1
        sheet.write_merge(
            row_num - 1, row_num, 0, 6,
            'Сводный отчёт по инвентаризации оборудования, находящегося на баллансе ОПФ РФ в Ленинском районе г. Севастополя',
            self.header_bold
        )

        row_num += 2
        sheet.write_merge(row_num, row_num, 0, 1, 'На дату: %s' % (date.today().strftime('%Y-%m-%d')))
        row_num += 2

        columns = [
            ('Инвентарный номер', 5000),
            ('Серийный номер', 6000),
            ('Тип оборудования', 5000),
            ('Модель оборудования', 12000),
            ('Месторасположение', 5000),
            ('Ответственный', 5000),
            ('Ревизия', 3000),
        ]

        for column_number in range(len(columns)):
            sheet.write(row_num, column_number, columns[column_number][0], self.header_style)
            sheet.col(column_number).width = columns[column_number][1]

        all_counter = 0

        for obj in self.queryset:
            row_num += 1

            for equipment in obj.equipment_set.all():
                row = [
                    equipment.inventory_number if equipment.inventory_number else 'Отсутствует',
                    equipment.serial_number,
                    equipment.type.value,
                    equipment.model,
                    equipment.responsible.location.emplacement,
                    equipment.responsible.short_full_name(),
                    datetime.strftime(equipment.revised_at, '%d.%m.%Y')
                ]

                all_counter += 1

                for column_number in range(len(row)):
                    sheet.write(row_num, column_number, row[column_number])

                row_num += 1

            if obj.types_count is not 0:
                sheet.write_merge(row_num, row_num, 0, 6,
                                  'Тип оборудования %s, всего: %s' % (obj.value, obj.types_count), self.group_style)
            else:
                row_num -= 1

        row_num += 2
        sheet.write_merge(row_num, row_num, 0, 6, 'Всего учтенного оборудования: %s единиц' % all_counter,
                          self.group_style)

        self.set_protection(sheet)
        self.workbook.save(self.response)
        return self.response


class XLS:
    ENCODING = 'utf-8'
    CONTENT_TYPE = 'application/vnd.ms-excel'
    INCREMENT_VALUE = 1
    SHEET_PASSWORD = '123'

    _row = 0

    sheet_header = ''
    sheet_name = 'Report'

    header_style = xlwt.easyxf('''
        font: bold on, height 200;
        pattern: pattern solid, fore_colour ice_blue;
        align: horiz center, vert center
    ''')
    date_style = xlwt.easyxf('''
        font: height 180, italic True;
        pattern: pattern solid, fore_colour white;
        alignment: horiz right, vert centre, wrap on;
        border: bottom thin, top thin;
    ''')
    dots_style = xlwt.easyxf('''
        pattern: pattern fine_dots;
    ''')
    columns_style = xlwt.easyxf('''
        alignment: horiz centre, vert centre, wrap on;
        font: bold on, height 200;
    ''')
    text_style = xlwt.easyxf('''
        alignment: vert centre, wrap on;
        font: height 140, color gray25;
    ''')
    no_value_style = xlwt.easyxf('''
        alignment: horz center, vert centre, wrap on;
        font: color red, bold True;
    ''')
    all_style = xlwt.easyxf('''
        alignment: horz right, vert centre, wrap on;
        font: bold True, height 220;
    ''')

    def __init__(self, sheet_name=''):
        self._response = XLS.get_response()
        self._workbook = xlwt.Workbook(encoding=XLS.ENCODING)
        self.sheet_name = sheet_name

    @staticmethod
    def get_response():
        response = HttpResponse(content_type=XLS.CONTENT_TYPE)
        response['Content-Disposition'] = 'attachment; filename=report_%s.xls' % XLS.get_datetime()
        return response

    @staticmethod
    def get_datetime(time=True):
        if time is False:
            return datetime.today().strftime('%Y-%m-%d')
        return datetime.today().strftime('%Y-%m-%d_%H%M%S')

    def set_protection(self):
        self._sheet.protect = True
        self._sheet.wnd_protect = True
        self._sheet.obj_protect = True
        self._sheet.scen_protect = True
        self._sheet.password = self.SHEET_PASSWORD

        self._workbook.protect = True
        self._workbook.wnd_protect = True
        self._workbook.obj_protect = True

    def increment_row(self, increment_value=INCREMENT_VALUE):
        self._row += increment_value
        return self._row

    def _create_sheet(self, cell_overwrite=False):
        self._sheet = self._workbook.add_sheet(self.sheet_name, cell_overwrite_ok=cell_overwrite)

    def add_merge_row(self, row_start, row_end, column_start, column_end, value='', style=None):
        self._sheet.write_merge(row_start, row_end, column_start, column_end, value, style)
        self._row += (row_end - row_start) + 1

    def render(self, queryset=None, columns=None):
        if not columns:
            columns = []
        self._create_sheet()

        # header row
        if self.sheet_header is not None:
            self.add_merge_row(self._row, self._row + 1, 0, len(columns) - 1, self.sheet_header,
                               self.header_style)

        # date row
        self.add_merge_row(self._row, self._row + 3, 0, len(columns) - 1, 'На дату: %s' % self.get_datetime(time=False),
                           style=self.date_style)

        # column names
        for index, column in enumerate(columns):
            self._sheet.write(self._row, index, column['repr'], self.columns_style)

            if 'size' in column:
                self._sheet.col(index).width = column['size']

        type_counter = 0
        # columns data
        for entity in queryset:
            self.increment_row()
            type_counter += 1

            row = []

            for column in columns:
                row.append(self.get_repr(self.get_field(entity, column['property'])))

            for column_number in range(len(row)):
                if row[column_number] is None:
                    self._sheet.write(self._row, column_number, 'Отсутствует', self.no_value_style)
                else:
                    self._sheet.write(self._row, column_number, str(row[column_number]))

        self.increment_row()
        self.add_merge_row(self._row, self._row, 0, len(columns) - 1, '', self.dots_style)
        self.add_merge_row(self._row, self._row, 0, len(columns) - 1, 'Всего: %s ед.' % type_counter, self.all_style)

        self.set_protection()
        self._workbook.save(self._response)
        return self._response

    @staticmethod
    def get_repr(value):
        if callable(value):
            return '%s' % value()
        return value

    @staticmethod
    def get_field(instance, field):
        field_path = field.split('.')
        attr = instance
        for elem in field_path:
            try:
                attr = getattr(attr, elem)
            except AttributeError:
                raise Exception('Wrong model or relation column attribute "%s"' % field)
        return attr
