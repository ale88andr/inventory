from io import BytesIO
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, TemplateView, DetailView

from employee.models import Location
from equipment.models.pdf_print import PdfPrint
from reports.models import XLS, PDF
from .models import Equipment, EquipmentTypes
from .forms import EquipmentFilterForm, EquipmentSearchForm


class EquipmentsView(ListView):
    model = Equipment
    paginate_by = 10
    context_object_name = 'equipments'
    template_name = 'equipment/list.html'
    page_title = 'Учтённое оборудование'

    def dispatch(self, request, *args, **kwargs):
        self.filter_form = EquipmentFilterForm(request.GET)
        self.filter_form.is_valid()

        self.search_form = EquipmentSearchForm(request.GET)
        self.search_form.is_valid()

        if 'pdf' in request.POST:
            return self.sticker_v2(request.POST.get('pdf'))

        if self.filter_form.cleaned_data.get('on_page'):
            self.paginate_by = int(self.filter_form.cleaned_data.get('on_page'))

        return super(EquipmentsView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(EquipmentsView, self).get_context_data(**kwargs)
        context['filter_form'] = self.filter_form
        context['search_form'] = self.search_form
        return context

    def get_queryset(self):
        if self.search_form.cleaned_data.get('search'):
            return Equipment.search_ng(self.search_form.cleaned_data.get('search'))
        else:
            queryset = Equipment.all()

        type_id = self.filter_form.cleaned_data.get('filter_type')
        responsible_id = self.filter_form.cleaned_data.get('filter_responsible')
        sort_by_item = self.filter_form.cleaned_data.get('sort_by')

        if type_id:
            queryset = queryset.filter(type=type_id)
        if responsible_id:
            queryset = queryset.filter(responsible=responsible_id)
        if sort_by_item:
            queryset = queryset.order_by(sort_by_item)

        return queryset

    @staticmethod
    def sticker_v2(equipment_id):
        equipment = Equipment.get(equipment_id)
        filename = 'sticker_' + equipment.serial_number
        pdf = PDF(fileName=filename)
        pdf.insertImage(equipment.generate_qrcode(pdf=True))
        pdf.insertRow('{0}'.format(equipment.inventory_number), 'h1_qr', lineBreak=False)
        pdf.insertRow('s/n {0}'.format(equipment.serial_number), 'center')
        return pdf.render()


class EquipmentTypesView(TemplateView):
    template_name = 'equipment/types.html'
    page_title = 'Типы оборудования'
    type_set_annotation = EquipmentTypes.annotation.all()


class DetailTypeView(DetailView):
    template_name = 'equipment/type.html'
    page_title = 'Оборудование: '
    context_object_name = 'type'
    queryset = EquipmentTypes.equipments.all()

    def get_context_data(self, **kwargs):
        context = super(DetailTypeView, self).get_context_data(**kwargs)
        self.page_title += self.object.value
        context['equipments_type_count'] = str(self.object.equipment_set.count())
        context['equipments'] = self.object.equipment_set.all
        return context

    def get(self, request, *args, **kwargs):
        if 'xls' in request.GET:
            return self._render_type_report(kwargs.get('pk'))
        return super(DetailTypeView, self).get(request, *args, **kwargs)

    @staticmethod
    def _render_type_report(type_pk):
        type_object = get_object_or_404(EquipmentTypes, pk=type_pk)
        equipments_set = type_object.equipment_set.all().select_related('responsible', 'responsible__location')
        columns = (
            {'repr': 'Модель оборудования', 'property': 'model', 'size': 12000},
            {'repr': 'Серийный №', 'property': 'serial_number', 'size': 4000},
            {'repr': 'Инвентарный №', 'property': 'inventory_number', 'size': 4000},
            {'repr': 'Расположение', 'property': 'responsible.location', 'size': 4000},
            {'repr': 'Ответственный', 'property': 'responsible', 'size': 5000}
        )
        xls = XLS(sheet_name=type_object.value)
        xls.sheet_header = 'Оборудование %s находящееся на баллансе' % type_object.value
        return xls.render(queryset=equipments_set, columns=columns)


class EquipmentLocationsView(TemplateView):
    template_name = 'equipment/locations.html'
    page_title = 'Расположение оборудования'
    locations_set = Location.annotation.all()


class DetailLocationView(DetailView):
    template_name = 'equipment/location.html'
    page_title = 'Месторасположение: '
    context_object_name = 'location'
    queryset = Location.objects.all()

    def get_context_data(self, **kwargs):
        context = super(DetailLocationView, self).get_context_data(**kwargs)
        self.page_title += self.object.emplacement
        context['equipments'] = Equipment.objects.filter(responsible__location_id=self.object.pk)
        context['equipments_location_count'] = str(context['equipments'].count())
        return context

    def get(self, request, *args, **kwargs):
        if 'xls' in request.GET:
            return self._render_type_report(kwargs.get('pk'))
        return super(DetailLocationView, self).get(request, *args, **kwargs)

    @staticmethod
    def _render_type_report(location_pk):
        location = Location.objects.get(pk=location_pk)
        equipments_set = Equipment.objects.filter(responsible__location_id=location_pk)
        columns = (
            {'repr': 'Тип оборудования', 'property': 'type.value', 'size': 6000},
            {'repr': 'Модель оборудования', 'property': 'model', 'size': 12000},
            {'repr': 'Серийный №', 'property': 'serial_number', 'size': 4000},
            {'repr': 'Инвентарный №', 'property': 'inventory_number', 'size': 4000},
            {'repr': 'Ответственный', 'property': 'responsible', 'size': 5000}
        )
        xls = XLS(sheet_name=location.emplacement)
        xls.sheet_header = 'Оборудование %s находящееся на баллансе' % location.emplacement
        return xls.render(queryset=equipments_set, columns=columns)
