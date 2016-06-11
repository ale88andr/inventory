from django.views.generic import TemplateView
from .forms import ReportsForm
from .models import Report


class ReportsView(TemplateView):
    template_name = 'reports/index.html'
    page_title = 'Отчёты'
    reports_form = ReportsForm()

    def get(self, request, *args, **kwargs):
        if request.GET.get('report_type') == 'summary':
            return Report(report_name='Суммарный отчёт', filename='sr').summary_report()

        return super(ReportsView, self).get(request, *args, **kwargs)
