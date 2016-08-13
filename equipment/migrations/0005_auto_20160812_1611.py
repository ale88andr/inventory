# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-08-12 13:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('equipment', '0004_auto_20160805_1536'),
    ]

    operations = [
        migrations.AlterField(
            model_name='equipment',
            name='inventory_number',
            field=models.CharField(blank=True, help_text='Инвентарный номер оборудования, допускаются только цифровые идентификаторы', max_length=30, null=True, verbose_name='Инвентарный номер'),
        ),
    ]
