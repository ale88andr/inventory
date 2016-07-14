from django.utils.translation import ugettext as _
from django.db import models

from enterprise.models.organisation import Organisation


class Department(models.Model):
    title = models.CharField(
        'Наименование',
        max_length=100,
        unique=True,
        db_index=True
    )
    organisation = models.ForeignKey(
        Organisation,
        verbose_name='Подразделение относится к'
    )

    @staticmethod
    def all():
        results = Department.objects.all()
        results = results.select_related('organisation')
        return results

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('Подразделение')
        verbose_name_plural = _('Подразделения')
        app_label = 'enterprise'
