from io import BytesIO

from django.http import HttpResponse
from django.views.generic import ListView

from equipment.models.pdf_print import PdfPrint
from .models import Equipment
from .forms import EquipmentFilterForm, EquipmentSearchForm


class EquipmentsView(ListView):
    model = Equipment
    paginate_by = 10
    context_object_name = 'equipments'
    template_name = 'equipment/equipments.html'
    page_title = 'Учтённое оборудование'

    def dispatch(self, request, *args, **kwargs):
        self.filter_form = EquipmentFilterForm(request.GET)
        self.filter_form.is_valid()

        self.search_form = EquipmentSearchForm(request.GET)
        self.search_form.is_valid()

        if 'pdf' in request.POST:
            return EquipmentsView.sticker(request.POST.get('pdf'))

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
    def sticker(equipment_id):
        equipment = Equipment.get(equipment_id)
        response = HttpResponse(content_type='application/pdf')
        filename = 'sticker_' + equipment.serial_number
        response['Content-Disposition'] = 'attachement; filename={0}.pdf'.format(filename)
        buffer = BytesIO()
        report = PdfPrint(buffer, 'Letter')
        pdf = report.report(
            equipment_qrcode=equipment.generate_qrcode(pdf=True),
            equipment_inventory=equipment.inventory_number,
            equipment_serial=equipment.serial_number
        )
        response.write(pdf)
        return response
