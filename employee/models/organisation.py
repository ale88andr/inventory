from django.utils.translation import ugettext as _
from django.db import models


class Organisation(models.Model):
    title = models.CharField(_('Наименование'), max_length=80, unique=True, db_index=True)
    short_title = models.CharField(_('Краткое наименование'), max_length=40, unique=True, null=True, blank=True)
    parent = models.ForeignKey('self', related_name='subordinates', default=0, blank=True, null=True, verbose_name='В подчинении')

    @staticmethod
    def all():
        return Organisation.objects.all()

    @staticmethod
    def get(pk):
        return Organisation.objects.get(pk=pk)

    def has_subordinates(self):
        if self.subordinates.count():
            return True

        return False

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('Организация')
        verbose_name_plural = _('Организации')
        app_label = 'employee'

