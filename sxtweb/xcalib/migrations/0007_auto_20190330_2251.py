# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-03-31 02:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('xcalib', '0006_auto_20190107_1120'),
    ]

    operations = [
        migrations.AlterField(
            model_name='calibration',
            name='Has_Pion_Ppol',
            field=models.BooleanField(default=False, verbose_name='User Specify Pion Ppol'),
        ),
    ]
