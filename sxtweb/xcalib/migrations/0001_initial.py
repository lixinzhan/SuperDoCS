# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-12-05 20:57
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('resources', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CALIBRATION',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('CalibName', models.CharField(max_length=32, unique=True, verbose_name='ID')),
                ('CalibrationMethod', models.CharField(choices=[('in-Air', 'TG61 in-Air method')], default='in-Air', max_length=32, verbose_name='Calibration Method')),
                ('Status', models.CharField(choices=[('Active', 'Active'), ('Disabled', 'Disabled')], default='Active', max_length=16)),
                ('FDD', models.FloatField(verbose_name='Focal Detector Dist. (cm)')),
                ('Pressure', models.FloatField(verbose_name='Pressure (mm Hg)')),
                ('Temperature', models.FloatField(verbose_name='Temperature (Celsius)')),
                ('BeamDuration', models.FloatField(verbose_name='Beam Duration (min or MU)')),
                ('V_std', models.FloatField(default=300, verbose_name='Standard Voltage')),
                ('M_std', models.FloatField(verbose_name='Reading Average (for V_std)')),
                ('V_opp', models.FloatField(default=-300, verbose_name='Opposite Voltage')),
                ('M_opp', models.FloatField(verbose_name='Reading Average (for V_opp)')),
                ('V_low', models.FloatField(default=150, verbose_name='Low Voltage')),
                ('M_low', models.FloatField(verbose_name='Reading Average (for V_low)')),
                ('MeasurementDate', models.DateField(verbose_name='Measured On')),
                ('MeasuredByUser', models.CharField(max_length=32, verbose_name='Measured By')),
                ('LastModifiedDateTime', models.DateTimeField(auto_now=True)),
                ('LastModifiedByUser', models.CharField(max_length=32, verbose_name='Last Modified By User')),
                ('Comment', models.TextField(blank=True, max_length=512)),
                ('P_elec', models.FloatField(default=1.0)),
                ('P_stem', models.FloatField(default=1.0, verbose_name='Stem Factor')),
                ('P_tp', models.FloatField(default=0.0)),
                ('P_pol', models.FloatField(default=0.0)),
                ('P_ion', models.FloatField(default=0.0)),
                ('P_isf', models.FloatField(default=0.0)),
                ('MassAbs_WatAir_air', models.FloatField(default=0.0, verbose_name='Mass Abs. Coeff. (Water to Air in Air)')),
                ('BSF_Wat', models.FloatField(default=0.0, verbose_name='Back Scattering Factor for Water')),
                ('BSF_ConeEnd', models.FloatField(default=0.0, verbose_name='BSF Correction Factor for Close-Ended Cone')),
                ('DR_Air', models.FloatField(default=0.0, verbose_name='Air Kerma Rate in Air')),
                ('DR_Water', models.FloatField(default=0.0, verbose_name='Dose Rate at Water Surface')),
                ('Cone', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='resources.CONE', verbose_name='Applicator')),
                ('Filter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='resources.FILTER')),
            ],
        ),
        migrations.CreateModel(
            name='LOCALSTANDARD',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('LocalStandardId', models.CharField(max_length=32, unique=True, verbose_name='Local Standard ID')),
                ('HVLUnit', models.CharField(choices=[('mm Al', 'mm Al'), ('mm Cu', 'mm Cu')], default='mm Al', max_length=16, verbose_name='HVL Unit')),
                ('HVL', models.FloatField(verbose_name='Calibration HVL')),
                ('Nx', models.FloatField(blank=True, default=0.0, verbose_name='Nx (R/rdg)')),
                ('Nk', models.FloatField(default=0.0, verbose_name='Nk (cGy/rdg)')),
                ('Status', models.CharField(choices=[('Active', 'Active'), ('Disabled', 'Disabled')], max_length=32)),
                ('CalibrationDate', models.DateField()),
                ('CalibratedBy', models.CharField(choices=[('NRC', 'NRC')], max_length=32, verbose_name='Calibrated By')),
                ('Comment', models.TextField(blank=True, max_length=256)),
                ('Chamber', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='resources.CHAMBER')),
                ('Electrometer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='resources.ELECTROMETER')),
            ],
            options={
                'verbose_name_plural': 'Local Standards',
            },
        ),
        migrations.CreateModel(
            name='MEASUREMENTSET',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('MeasurementSetId', models.CharField(max_length=32, unique=True, verbose_name='Meas Set Id')),
                ('M_LS', models.FloatField(default=0.0, verbose_name='Local Std Rdg')),
                ('M_MS', models.FloatField(default=0.0, verbose_name='Current Set Rdg')),
                ('XCalFactor', models.FloatField(default=0.0)),
                ('Nx', models.FloatField(blank=True, default=0.0, verbose_name='Nx (R/rdg)')),
                ('Nk', models.FloatField(blank=True, default=0.0, verbose_name='Nk (cGy/rdg)')),
                ('Status', models.CharField(choices=[('Active', 'Active'), ('Disabled', 'Disabled')], max_length=32)),
                ('CalibrationDate', models.DateField()),
                ('CalibratedByUser', models.CharField(max_length=32)),
                ('Comment', models.TextField(blank=True, max_length=256)),
                ('Chamber', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='resources.CHAMBER')),
                ('Cone', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='resources.CONE', verbose_name='Applicator')),
                ('Electrometer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='resources.ELECTROMETER')),
                ('Filter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='resources.FILTER')),
                ('LocalStandard', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='xcalib.LOCALSTANDARD')),
            ],
            options={
                'verbose_name_plural': 'Measurement Sets',
            },
        ),
        migrations.CreateModel(
            name='NOMINALCALIBRATION',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('NCalibName', models.CharField(max_length=32, unique=True, verbose_name='Nominal Calib. Name')),
                ('Status', models.CharField(choices=[('Active', 'Active'), ('Disabled', 'Disabled')], default='Active', max_length=16)),
                ('DR_Air', models.FloatField(default=0.0, verbose_name='Air Kerma Rate in Air')),
                ('DR_Water', models.FloatField(default=0.0, verbose_name='Dose Rate at Water Surface')),
                ('LastModifiedDateTime', models.DateTimeField(auto_now=True)),
                ('LastModifiedByUser', models.CharField(max_length=32, verbose_name='Last Modified By User')),
                ('Comment', models.TextField(blank=True, max_length=512)),
                ('Cone', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='resources.CONE')),
                ('Filter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='resources.FILTER')),
            ],
            options={
                'verbose_name': 'Nominal Calibrations',
            },
        ),
        migrations.CreateModel(
            name='OUTPUTFACTOR',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ROFName', models.CharField(max_length=32, unique=True, verbose_name='ID')),
                ('FitMethod', models.CharField(choices=[('Default', 'Default'), ('Customized', 'Customized')], max_length=32, verbose_name='Curve Fitting Method')),
                ('ConeFactor', models.FloatField(default=0, verbose_name='Cone Factor')),
                ('DequivMax', models.FloatField(default=0, verbose_name='Max Allowed Equiv. Diameter (cm)')),
                ('DequivMin', models.FloatField(default=0, verbose_name='Min Allowed Equiv. Diameter (cm)')),
                ('CutoutThickness', models.FloatField(default=0.2, verbose_name='Cutout Thickness (cm)')),
                ('P', models.FloatField(default=0)),
                ('S', models.FloatField(default=0)),
                ('L', models.FloatField(default=0)),
                ('U', models.FloatField(default=0)),
                ('N', models.FloatField(default=0)),
                ('A', models.FloatField(default=0)),
                ('B', models.FloatField(default=0)),
                ('C', models.FloatField(default=0)),
                ('D', models.FloatField(default=0)),
                ('E', models.FloatField(default=0)),
                ('F', models.FloatField(default=0)),
                ('G', models.FloatField(default=0)),
                ('Cone', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='resources.CONE', verbose_name='Applicator')),
                ('Filter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='xcalib.CALIBRATION', verbose_name="Calib'd Filter")),
            ],
            options={
                'verbose_name_plural': 'Output Factors',
            },
        ),
        migrations.AddField(
            model_name='calibration',
            name='MeasurementSet',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='xcalib_calibration_MeasurementSet', to='xcalib.MEASUREMENTSET', verbose_name='Measurement Set'),
        ),
    ]
