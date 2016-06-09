from django.views.generic import TemplateView
from .forms import ReportsForm


class ReportsView(TemplateView):
    template_name = 'reports/index.html'
    page_title = 'Отчёты'
    reports_form = ReportsForm()

