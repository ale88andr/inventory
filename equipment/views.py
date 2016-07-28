# coding=utf-8
import csv
import json
from collections import namedtuple

from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.utils.decorators import method_decorator
from django.utils.functional import cached_property
from django.views.generic import ListView, TemplateView, DetailView, UpdateView, FormView

from enterprise.models import Location
from reports.models import XLS, PDF
from .models import Equipment, EquipmentTypes
from .forms import EquipmentFilterForm, EquipmentSearchForm, EquipmentChownForm, UploadFileForm


class EquipmentFormMixin(object):

    def forms(self):
        """Returns a dictionary of filter and search form object"""
        filter = self.filter_form
        search = self.search_form
        return {
            'filter': filter,
            'search': search
        }

    def page(self):
        """Returns a dictionary of page properties"""
        title = 'Оборудование на баллансе'
        return {
            'title': title
        }


class EquipmentIndexView(ListView, EquipmentFormMixin):
    model = Equipment
    paginate_by = 10
    context_object_name = 'equipments'
    template_name = 'equipment/list.html'

    def dispatch(self, request, *args, **kwargs):
        self.filter_form = EquipmentFilterForm(request.GET)
        self.filter_form.is_valid()

        self.search_form = EquipmentSearchForm(request.GET)
        self.search_form.is_valid()

        if 'pdf' in request.POST:
            return self.sticker_v2(request.POST.get('pdf'))

        if self.filter_form.cleaned_data.get('on_page'):
            self.paginate_by = int(self.filter_form.cleaned_data.get('on_page'))

        return super(EquipmentIndexView, self).dispatch(request, *args, **kwargs)

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
        if equipment.inventory_number:
            pdf.insertRow('{0}'.format(equipment.inventory_number), 'h1_qr', lineBreak=False)
        pdf.insertRow('s/n {0}'.format(equipment.serial_number), 'center')
        return pdf.render()


class EquipmentTypesView(TemplateView):
    template_name = 'equipment/types.html'
    page_title = 'Типы оборудования'
    type_set_annotation = EquipmentTypes.annotation.all()


class EquipmentTypeMixin(object):

    @cached_property
    def equipments(self):
        """Returns a dictionary of type equipments"""
        selection = self.object.equipment_set
        return {
            'selection': selection.all(),
            'count': selection.count()
        }

    def page(self):
        """Returns a dictionary of page properties"""
        title = 'Оборудование: {0}'.format(self.object.value)
        return {
            'title': title
        }


class EquipmentTypeView(DetailView, EquipmentTypeMixin):
    template_name = 'equipment/type.html'
    context_object_name = 'type'
    queryset = EquipmentTypes.equipments.all()

    def get(self, request, *args, **kwargs):
        if 'xls' in request.GET:
            return self._render_type_report(kwargs.get('pk'))
        return super(EquipmentTypeView, self).get(request, *args, **kwargs)

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

    def locations(self):
        selection = Location.annotation.all()
        return {
            'selection': selection
        }

    def page(self):
        return {
            'title': 'Распределение оборудования по месторасположению'
        }


class EquipmentEmplacementMixin(object):

    @cached_property
    def equipments(self):
        """Returns a dictionary of equipments by location"""
        selection = Equipment.objects.filter(responsible__location_id=self.object.id)
        return {
            'selection': selection,
            'count': selection.count()
        }

    def page(self):
        """Returns a dictionary of page properties"""
        title = 'Месторасположение:  {0}'.format(self.object.emplacement)
        return {
            'title': title
        }


class EquipmentEmplacementView(DetailView, EquipmentEmplacementMixin):
    template_name = 'equipment/location.html'
    context_object_name = 'location'
    queryset = Location.objects.all()

    def get(self, request, *args, **kwargs):
        if 'xls' in request.GET:
            return self._render_type_report(kwargs.get('pk'))
        return super(EquipmentEmplacementView, self).get(request, *args, **kwargs)

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


class EquipmentChownMixin(object):

    def forms(self):
        """Returns a dictionary of edit form object"""
        edit = EquipmentChownForm
        return {
            'edit': edit,
        }

    def page(self):
        """Returns a dictionary of page properties"""
        title = 'Передача оборудования: {0}'.format(self.object.model)
        return {
            'title': title
        }


@method_decorator(login_required, name='dispatch')
class EquipmentChownView(UpdateView, EquipmentChownMixin):
    template_name = 'equipment/chown.html'
    model = Equipment
    context_object_name = 'equipment'
    fields = ['responsible']
    success_url = '/equipments/'


# @method_decorator(login_required, name='dispatch')
class EquipmentReviseView(FormView):
    form_class = UploadFileForm
    template_name = 'equipment/revise.html'
    # success_url = reverse_lazy('equipment:revise_confirmation')

    def page(self):
        return {
            'title': 'Создание новой ревизии'
        }

    def post(self, request, *args, **kwargs):

        if request.is_ajax():
            form = UploadFileForm(request.POST, request.FILES)

            if form.is_valid():
                file = form.cleaned_data['file']
                file_extension = file.name.split('.')[-1]

                if file_extension is not 'csv' or file.content_type is not 'application/vnd.ms-excel':
                    form.add_error('file', 'Загруженный файл имеет неправильный формат.')

                file = request.FILES['file'].read().decode().splitlines()
                revise = csv.DictReader(file, delimiter=';', dialect=csv.excel_tab)

                # Qrdata = namedtuple('Qrdata', ['model', 'iventory_number', 'serial_number', 'revised_at'])

                data = []

                try:
                    for row in revise:
                        model, i_number, s_number = row.get('QR_DATA').split(', ')
                        data.append({
                            'model': model,
                            'inventory_number': i_number.split(':')[-1],
                            'serial_number': s_number.split(':')[-1],
                            'revised_at': row.get('DATE')
                        })
                        # qr_data = (model, i_number.split(':')[-1], s_number.split(':')[-1], row.get('DATE'))
                        # self.data.append(Qrdata._make(qr_data)._asdict())
                except(ValueError, KeyError):
                    form.add_error('file', 'Загруженный файл ревизии имеет неправильную структуру')

                return HttpResponse(
                    json.dumps(data),
                    content_type="application/json"
                )
            else:
                return HttpResponse(
                    json.dumps({"errors": form.errors}),
                    content_type="application/json",
                    status=400
                )


# @method_decorator(login_required, name='dispatch')
# class EquipmentReviseConfirmView(TemplateView):
#     template_name = 'equipment/revise_transitional.html'
