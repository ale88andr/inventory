from django.utils.translation import ugettext as _
from django.db import models


class Organisation(models.Model):
    title = models.CharField(_('Наименование'), max_length=80, unique=True, db_index=True)
    parent = models.ForeignKey('Organisation', default=0, blank=True, null=True, verbose_name='В подчинении')

    @staticmethod
    def all():
        return Organisation.objects.all()

    @staticmethod
    def get(pk):
        return Organisation.objects.get(pk=pk)

    def has_subordinates(self):
        if len(self.subordinates()):
            return True

        return False

    def subordinates(self):
        return Organisation.all().filter(parent=self.pk)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('Организация')
        verbose_name_plural = _('Организации')
        app_label = 'employee'

