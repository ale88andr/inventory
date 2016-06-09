from django.views.generic import ListView

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
