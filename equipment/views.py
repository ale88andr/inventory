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
        self.search_form = EquipmentSearchForm(request.GET)
        self.search_form.is_valid()

        if self.search_form.cleaned_data.get('on_page'):
            self.paginate_by = int(self.search_form.cleaned_data.get('on_page'))

        return super(EquipmentsView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(EquipmentsView, self).get_context_data(**kwargs)
        context['search_form'] = self.search_form
        return context

    def get_queryset(self):
        queryset = Equipment.all()

        if self.search_form.cleaned_data.get('filter_type'):
            queryset = queryset.filter(type=self.search_form.cleaned_data.get('filter_type'))
        if self.search_form.cleaned_data.get('filter_responsible'):
            queryset = queryset.filter(responsible=self.search_form.cleaned_data.get('filter_responsible'))
        if self.search_form.cleaned_data.get('sort_by'):
            queryset = queryset.order_by(self.search_form.cleaned_data.get('sort_by'))

        return queryset
