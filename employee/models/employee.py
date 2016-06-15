from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext as _
from django.db import models

from employee.models.organisation import Organisation
from employee.models.location import Location
from employee.models.departments import Department


class Employee(models.Model):

    STATES = [
        [True, _('Работает')],
        [False, _('Уволен')]
    ]

    POSITIONS = [
        [1, _('Специалист-эксперт')],
        [2, _('Ведущий специалист-эксперт')],
        [3, _('Главный специалист-эксперт')],
        [4, _('Старший инспектор')],
        [5, _('Специалист-эксперт (по автоматизации)')],
        [6, _('Руководитель группы')],
        [7, _('Заместитель начальника отдела')],
        [8, _('Начальник отдела')],
        [9, _('Ведущий специалист-эксперт (юрисконсульт)')],
        [10, _('Руководитель клиентской службы')],
        [11, _('Архивариус')],
    ]

    surname = models.CharField(_('Фамилия'), max_length=50, db_index=True)
    firstname = models.CharField(_('Имя'), max_length=25)
    middlename = models.CharField(_('Отчество'), max_length=25)
    organisation = models.ForeignKey(Organisation, verbose_name='Сотрудник организации')
    department = models.ForeignKey(Department, verbose_name='Подразделение', blank=True, null=True)
    phone = models.CharField(_('Телефон'), max_length=25, blank=True, null=True)
    location = models.ForeignKey(Location, verbose_name='Месторасположение', blank=True, null=True)
    updated_at = models.DateTimeField(_('Дата последнего изменения'), auto_now=True)
    created_at = models.DateTimeField(_('Дата создания'), auto_now_add=True)
    state = models.BooleanField(_('Состояние'), choices=STATES, default=True)
    position = models.IntegerField(_('Должность'), choices=POSITIONS, default=1)

    def full_name(self):
        return '%s %s %s' % (self.surname, self.firstname, self.middlename)

    def short_full_name(self):
        return '%s %s. %s.' % (self.surname, self.firstname[:1], self.middlename[:1])

    def info(self):
        return '%s(%s, %s)' % (self.full_name(), self.organisation.title, self.location.emplacement)

    @staticmethod
    def all():
        return Employee.objects.select_related('organisation', 'department', 'location').all()

    @staticmethod
    def get(pk):
        return get_object_or_404(Employee, pk=pk)

    def __str__(self):
        return self.short_full_name()

    class Meta:
        verbose_name = _('Сотрудник')
        verbose_name_plural = _('Сотрудники')
        ordering = ['id']
        app_label = 'employee'
