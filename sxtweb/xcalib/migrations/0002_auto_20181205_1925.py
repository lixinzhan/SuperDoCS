# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-12-06 00:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('xcalib', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='measurementset',
            name='MeasurementSetId',
        ),
        migrations.AddField(
            model_name='measurementset',
            name='MSetName',
            field=models.CharField(default='MS', max_length=32, unique=True, verbose_name='Meas Set Name'),
            preserve_default=False,
        ),
    ]
