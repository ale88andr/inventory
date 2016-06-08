from django.db import models


class EquipmentTypes(models.Model):
    value = models.CharField('Значение', max_length=50, unique=True, db_index=True)

    @staticmethod
    def all():
        return EquipmentTypes.objects.all()

    def __str__(self):
        return self.value

    class Meta:
        verbose_name = 'Тип оборудования'
        verbose_name_plural = 'Типы оборудования'
        app_label = 'equipment'
        ordering = ['value']
