from django.views.generic import ListView

from .models import Equipment


class EquipmentsView(ListView):
    model = Equipment
    paginate_by = 1
    context_object_name = 'equipments'
    template_name = 'equipment/equipments.html'

    def get_queryset(self):
        return Equipment.all()
