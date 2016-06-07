from django.utils.translation import ugettext as _
from django.db import models

from employee.models.organisation import Organisation


class Location(models.Model):
    emplacement = models.CharField(_('Расположение'), max_length=50, db_index=True, unique=True)
    organisation = models.ForeignKey(Organisation, verbose_name='Находится в организации')
    is_active = models.BooleanField(_('Активно?'), default=True)

    def __str__(self):
        return self.emplacement

    class Meta:
        verbose_name = _('Месторасположение')
        verbose_name_plural = _('Месторасположения')
        app_label = 'employee'
