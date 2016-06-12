from datetime import date, datetime
import xlwt
from django.db.models import Count
from django.http import HttpResponse
from django.utils import timezone
from equipment.models.equipment import Equipment
from equipment.models.equipment_types import EquipmentTypes


class Report:

    encoding = 'utf-8'
    content_type = 'application/vnd.ms-excel'
    sheet_password = '123'

    std_font = xlwt.Font()
    std_font.name = ''
    std_font.bold = True
    std_font.height = 140


    header_bold = xlwt.easyxf("font: bold on, height 200; pattern: pattern solid, fore_colour ice_blue; align: horiz center, vert center")
    header_style = xlwt.easyxf("font: bold on, height 160; pattern: pattern solid, fore_colour ice_blue; align: horiz center")
    group_style = xlwt.easyxf("font: bold True; pattern: pattern solid, fore_colour ice_blue; align: horiz right")
    group_style_l = xlwt.easyxf("font: bold True; pattern: pattern solid, fore_colour ice_blue; align: horiz left")

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
            row_num-1, row_num, 0, 6,
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

                for column_number in range(len(row)):
                    sheet.write(row_num, column_number, row[column_number])

                row_num += 1

            if obj.types_count is not 0:
                sheet.write_merge(row_num, row_num, 0, 6, 'Тип оборудования %s, всего: %s' % (obj.value, obj.types_count), self.group_style)
            else:
                row_num -= 1

        self.set_protection(sheet)
        self.workbook.save(self.response)
        return self.response
