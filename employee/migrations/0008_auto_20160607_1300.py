# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-07 10:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0007_auto_20160607_1259'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organisation',
            name='short_title',
            field=models.CharField(blank=True, max_length=40, null=True, unique=True, verbose_name='Краткое наименование'),
        ),
    ]