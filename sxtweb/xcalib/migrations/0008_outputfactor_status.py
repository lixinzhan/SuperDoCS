# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-03-31 03:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('xcalib', '0007_auto_20190330_2251'),
    ]

    operations = [
        migrations.AddField(
            model_name='outputfactor',
            name='Status',
            field=models.CharField(choices=[('Active', 'Active'), ('Disabled', 'Disabled')], default='Active', max_length=16),
        ),
    ]
