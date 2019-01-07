# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2019-01-07 16:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('xcalib', '0005_auto_20181207_1159'),
    ]

    operations = [
        migrations.AddField(
            model_name='calibration',
            name='DurationUnit',
            field=models.CharField(choices=[('min', 'Minutes'), ('MU', 'Monitor Units')], default='MU', max_length=16, verbose_name='Duration Unit'),
        ),
        migrations.AddField(
            model_name='calibration',
            name='Has_Pion_Ppol',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='calibration',
            name='BeamDuration',
            field=models.FloatField(verbose_name='Beam Duration'),
        ),
        migrations.AlterField(
            model_name='calibration',
            name='P_isf',
            field=models.FloatField(default=0.0, verbose_name='Inverse Square Factor'),
        ),
        migrations.AlterField(
            model_name='outputfactor',
            name='FitMethod',
            field=models.CharField(choices=[('Default', 'Hill-Exponential'), ('Exponential', 'Exponential'), ('Hill', 'Hill'), ('Polynomial2', 'Polynomial2'), ('Polynomial3', 'Polynomial3'), ('Linear', 'Linear'), ('Customized', 'Customized')], max_length=32, verbose_name='Curve Fitting Method'),
        ),
    ]
