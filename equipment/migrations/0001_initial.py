# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-07-14 12:36
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('enterprise', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Equipment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('serial_number', models.CharField(blank=True, help_text='Заводской номер оборудования, может содержать цифры и символы, допускается его отсутствие', max_length=25, null=True, verbose_name='Серийный номер')),
                ('inventory_number', models.IntegerField(blank=True, help_text='Инвентарный номер оборудования, допускаются только цифровые идентификаторы', null=True, verbose_name='Инвентарный номер')),
                ('model', models.CharField(help_text='Марка оборудования, модель или другая информация', max_length=100, verbose_name='Модель')),
                ('note', models.TextField(blank=True, null=True, verbose_name='Примечание')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Созданно')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Обновленно')),
                ('revised_at', models.DateTimeField(blank=True, help_text='Дата проведения последней ревизии', null=True, verbose_name='Ревизия')),
                ('responsible', models.ForeignKey(help_text='Сотрудник ПФР за которым закрепленна техника', on_delete=django.db.models.deletion.CASCADE, to='enterprise.Employee', verbose_name='Ответственное лицо')),
            ],
            options={
                'verbose_name_plural': 'Учётные единицы',
                'verbose_name': 'Оборудование',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='EquipmentTypes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(db_index=True, max_length=50, unique=True, verbose_name='Значение')),
            ],
            options={
                'verbose_name_plural': 'Типы оборудования',
                'verbose_name': 'Тип оборудования',
                'ordering': ['value'],
            },
            managers=[
                ('annotation', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AddField(
            model_name='equipment',
            name='type',
            field=models.ForeignKey(help_text='Выберите к какому типу принадлежит создаваемое оборудование', on_delete=django.db.models.deletion.CASCADE, to='equipment.EquipmentTypes', verbose_name='Тип оборудования'),
        ),
    ]
