import base64
import qrcode
from io import BytesIO
from itertools import chain
from django.utils import timezone
from django.db import models
from equipment.models.equipment_types import EquipmentTypes
from enterprise.models.employee import Employee


class EquipmentsManager(models.Manager):

    def by_type(self, type_pk):
        return self.filter(type=type_pk)


class Equipment(models.Model):

    type = models.ForeignKey(
        EquipmentTypes,
        verbose_name='Тип оборудования',
        help_text='Выберите к какому типу принадлежит создаваемое оборудование'
    )
    serial_number = models.CharField(
        'Серийный номер',
        max_length=25,
        blank=True,
        help_text='Заводской номер оборудования, может содержать цифры и символы, допускается его отсутствие'
    )
    inventory_number = models.IntegerField(
        'Инвентарный номер',
        blank=True,
        help_text='Инвентарный номер оборудования, допускаются только цифровые идентификаторы'
    )
    model = models.CharField(
        'Модель',
        max_length=100,
        help_text='Марка оборудования, модель или другая информация'
    )
    responsible = models.ForeignKey(
        Employee,
        verbose_name='Ответственное лицо',
        help_text='Сотрудник ПФР за которым закрепленна техника'
    )
    note = models.TextField(
        'Примечание',
        blank=True,
    )
    created_at = models.DateTimeField(
        'Созданно',
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        'Обновленно',
        auto_now=True
    )
    revised_at = models.DateTimeField(
        'Ревизия',
        blank=True,
        null=True,
        help_text='Дата проведения последней ревизии'
    )

    objects = EquipmentsManager()

    def generate_qrcode(self, pdf=False):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=6,
            border=0,
        )
        qr_data = {'model': self.model, 'in': self.inventory_number, 'sn': self.serial_number}
        qr.add_data('{model} IN:{in} S/N:{sn}'.format(**qr_data))
        qr.make(fit=True)

        img = qr.make_image()

        buffer = BytesIO()
        img.save(buffer, 'PNG')

        if pdf:
            return buffer

        return base64.b64encode(buffer.getvalue())

    def revised_diff(self):
        date_diff = timezone.now() - self.revised_at

        if date_diff.days == 0:
            return '~ {0} ч. назад'.format(round(date_diff.seconds / 3600))

        return '{0} дн. назад'.format(date_diff.days)

    @staticmethod
    def all():
        results = Equipment.objects.all()
        results = results.select_related(
            'type', 'responsible__location', 'responsible__department', 'responsible', 'responsible__organisation'
        )
        return results

    @staticmethod
    def get(id):
        return Equipment.objects.get(id=id)

    @staticmethod
    def search_ng(text):
        qs = Equipment.all()

        serial_search = qs.filter(serial_number__icontains=text)
        model_search = qs.filter(model__icontains=text)
        inventory_search = ''

        if text is int:
            inventory_search = qs.filter(inventory_number__in=text)

        return list(chain(serial_search, model_search, inventory_search))

    def __str__(self):
        return self.model

    class Meta:
        verbose_name = 'Оборудование'
        verbose_name_plural = 'Учётные единицы'
        app_label = 'equipment'
        ordering = ['-created_at']
