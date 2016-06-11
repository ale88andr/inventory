from datetime import date
import xlwt
from django.db.models import Count
from django.http import HttpResponse
from equipment.models.equipment import Equipment
from equipment.models.equipment_types import EquipmentTypes


class Report:

    encoding = 'utf-8'

    header_bold = xlwt.easyxf("font: bold on, height 200; pattern: pattern solid, fore_colour ice_blue; align: horiz center")
    header_style = xlwt.easyxf("font: bold on, height 160; pattern: pattern solid, fore_colour ice_blue; align: horiz center")
    group_style = xlwt.easyxf("font: bold True; pattern: pattern solid, fore_colour sea_green; align: horiz right")
    group_style_l = xlwt.easyxf("font: bold True; pattern: pattern solid, fore_colour sea_green; align: horiz left")

    def __init__(self, filename, report_name):
        self.queryset = EquipmentTypes.objects.all().annotate(types_count=Count('equipment'))
        self.response = HttpResponse(content_type='application/ms-excel')
        self.response['Content-Disposition'] = 'attachment; filename=%s.xls' % filename
        self.report_name = report_name

    def summary_report(self):

        workbook = xlwt.Workbook(encoding=self.encoding)
        sheet = workbook.add_sheet(self.report_name, cell_overwrite_ok=True)

        row_num = 0
        sheet.write_merge(
            row_num, row_num, 0, 5,
            'Сводный отчёт по инвентаризации оборудования, находящегося на баллансе ОПФ РФ в Ленинском районе г. Севастополя',
            self.header_bold
        )

        row_num += 2
        sheet.write_merge(row_num, row_num, 0, 2, 'На дату %s' % (date.today().strftime('%Y-%m-%d')))
        row_num += 2

        columns = [
            ('Инвентарный номер', 5000),
            ('Серийный номер', 6000),
            ('Тип оборудования', 5000),
            ('Модель оборудования', 12000),
            ('Месторасположение', 5000),
            ('Ответственный', 5000),
        ]

        for column_number in range(len(columns)):
            sheet.write(row_num, column_number, columns[column_number][0], self.header_style)
            sheet.col(column_number).width = columns[column_number][1]

        for obj in self.queryset:
            row_num += 1

            for equipment in obj.equipment_set.all():
                row = [
                    equipment.inventory_number,
                    equipment.serial_number,
                    equipment.type.value,
                    equipment.model,
                    equipment.responsible.location.emplacement,
                    equipment.responsible.short_full_name()
                ]

                for column_number in range(len(row)):
                    sheet.write(row_num, column_number, row[column_number])

                row_num += 1
                sheet.write(row_num, 3, 'Всего по типу:', self.group_style)
                sheet.write(row_num, 4, obj.value, self.group_style_l)
                sheet.write(row_num, 5, obj.types_count, self.group_style)

        workbook.save(self.response)
        return self.response
