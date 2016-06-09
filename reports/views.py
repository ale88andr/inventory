from django.views.generic import TemplateView
from equipment.models.equipment import Equipment


class ReportsView(TemplateView):
    template_name = 'reports/index.html'
    page_title = 'Отчёты'
