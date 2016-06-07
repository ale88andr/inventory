from django.utils.translation import ugettext as _
from django.db import models

from employee.models.organisation import Organisation


class Department(models.Model):
    title = models.CharField(_('Наименование'), max_length=100, unique=True, db_index=True)
    organisation = models.ForeignKey(Organisation, verbose_name='Подразделение относится к')

    @staticmethod
    def all():
        return Department.objects.select_related('organisation').all()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('Подразделение')
        verbose_name_plural = _('Подразделения')
        app_label = 'employee'

