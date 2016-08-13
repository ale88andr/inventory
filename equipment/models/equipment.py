import base64
from datetime import datetime

import qrcode
from io import BytesIO
from itertools import chain
from django.utils import timezone
from django.db import models
from django.utils.timezone import localtime, get_current_timezone
from django.db import transaction

from equipment.models.equipment_types import EquipmentTypes
from enterprise.models.employee import Employee


class EquipmentsManager(models.Manager):

    def by_type(self, type_pk):
        return self.filter(type=type_pk)

    def unused(self):
        return self.filter(is_used=False)

    def in_repair(self):
        return self.filter(is_repair=True)

    def unrecorded(self):
        return self.filter(inventory_number=None)


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
    inventory_number = models.CharField(
        'Инвентарный номер',
        blank=True,
        null=True,
        max_length=30,
        help_text='Инвентарный номер оборудования, допускаются только цифровые идентификаторы'
    )
    model = models.CharField(
        'Модель',
        max_length=100,
        help_text='Марка оборудования, модель или другая информация'
    )
    responsible = models.ForeignKey(
        Employee,
        blank=True,
        null=True,
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
    is_used = models.BooleanField(
        'Используется',
        default=True
    )
    is_repair = models.BooleanField(
        'В ремонте',
        default=False
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
        qr.add_data('{model}, IN:{in}, S/N:{sn}'.format(**qr_data))
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
            hours = round(date_diff.seconds / 3600)
            if hours < 1:
                return '{0} мин. назад'.format(round(date_diff.seconds / 60))
            return '~ {0} ч. назад'.format(hours)

        return '{0} дн. назад'.format(date_diff.days)

    @staticmethod
    @transaction.atomic
    def update_equipments_revise(revise_equipments):

        for equipment in revise_equipments:
            inventory, serial, revised_at = equipment.split(';')
            revised_at = datetime.strptime(revised_at, '%d.%m.%Y %H:%M')
            equipments = Equipment.objects.all()

            if inventory == 'None':
                equipment_object = equipments.filter(serial_number=serial).first()
            else:
                equipment_object = equipments.filter(inventory_number=inventory).first()

            if localtime(equipment_object.revised_at) == revised_at.replace(tzinfo=get_current_timezone()):
                break

            equipment_object.revised_at = revised_at
            equipment_object.save(update_fields=['revised_at'])

    @staticmethod
    def all():
        results = Equipment.objects.all()
        results = results.select_related(
            'type', 'responsible__location', 'responsible__department', 'responsible', 'responsible__organisation'
        )
        return results

    @staticmethod
    def get(equipment_id):
        return Equipment.objects.get(id=equipment_id)

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
