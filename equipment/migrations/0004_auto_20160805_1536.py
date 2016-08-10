# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-08-05 12:36
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('equipment', '0003_auto_20160805_1535'),
    ]

    operations = [
        migrations.AlterField(
            model_name='equipment',
            name='responsible',
            field=models.ForeignKey(blank=True, help_text='Сотрудник ПФР за которым закрепленна техника', null=True, on_delete=django.db.models.deletion.CASCADE, to='enterprise.Employee', verbose_name='Ответственное лицо'),
        ),
    ]
