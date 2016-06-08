from django.views.generic import ListView

from .models import Equipment
from .forms import EquipmentSearchForm


class EquipmentsView(ListView):
    model = Equipment
    paginate_by = 10
    context_object_name = 'equipments'
    template_name = 'equipment/equipments.html'
    page_title = 'Учтённое оборудование'

    def dispatch(self, request, *args, **kwargs):
        self.filter_form = EquipmentSearchForm(request.GET)
        self.filter_form.is_valid()

        if self.filter_form.cleaned_data.get('on_page'):
            self.paginate_by = int(self.filter_form.cleaned_data.get('on_page'))

        return super(EquipmentsView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(EquipmentsView, self).get_context_data(**kwargs)
        context['filter_form'] = self.filter_form
        return context

    def get_queryset(self):
        queryset = Equipment.all()

        if self.filter_form.cleaned_data.get('filter_type'):
            queryset = queryset.filter(type=self.filter_form.cleaned_data.get('filter_type'))
        if self.filter_form.cleaned_data.get('filter_responsible'):
            queryset = queryset.filter(responsible=self.filter_form.cleaned_data.get('filter_responsible'))
        if self.filter_form.cleaned_data.get('sort_by'):
            queryset = queryset.order_by(self.filter_form.cleaned_data.get('sort_by'))

        return queryset
