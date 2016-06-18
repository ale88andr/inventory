from django.db import models


class EquipmentTypesAnnotation(models.Manager):
    def get_queryset(self):
        return super(EquipmentTypesAnnotation, self).get_queryset().annotate(types_count=models.Count('equipment'))


class EquipmentsTypeManager(models.Manager):
    def get_queryset(self):
        return super(EquipmentsTypeManager, self).get_queryset().prefetch_related(
            'equipment_set', 'equipment_set__responsible', 'equipment_set__responsible__location'
        )


class EquipmentTypes(models.Model):
    value = models.CharField('Значение', max_length=50, unique=True, db_index=True)

    # model Manager: EquipmentTypesAnnotation
    annotation = EquipmentTypesAnnotation()
    equipments = EquipmentsTypeManager()
    objects = models.Manager()

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
