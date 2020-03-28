#! /usr/bin/python
# -*- encoding: utf-8 -*-

import os
import math
import datetime
import numpy as np
import urllib.parse

from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import Context, RequestContext
from django.template.loader import get_template
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.utils.translation import ugettext_lazy as _

from .models import *
from .forms import *
from .curve_fitting import getROF
from common.errcode import ErrorCode

from protocols.TG61.CMedWat import CMedWat
from protocols.TG61.BSF_Wat import BSF_Wat
from protocols.TG61.BSF_CloseCone import BSF_CloseCone
from protocols.TG61.BSF_BoneWat import BSF_BoneWat
from protocols.TG61.Mu_WatAir_air import Mu_WatAir_air

import xhtml2pdf.pisa as pisa
from io import StringIO, BytesIO
import cgi
import csv
import hashlib
import platform

#@login_required
def pdf_export_page(request, planid):    
    if planid=='new' or planid=='0':
        return HttpResponseRedirect(reverse(plan_search_page))

    plan = get_object_or_404(TREATMENTPLAN, pk=planid)

    if os.path.isfile('user_templates/pdf_export_page.html'):
        template = get_template('user_templates/pdf_export_page.html')
    else:
        template = get_template('pdf_export_page.html')
        
    result = BytesIO()
    # context = Context({'plan':plan, 'VERSION': settings.VERSION })
    context = {'pagesize': 'Letter', 'plan':plan, 'settings': settings }
    html  = template.render(context)
    # pdf = pisa.pisaDocument(StringIO(html.encode("ISO-8859-1")), result,encod='ISO-8859-1')
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)

    if not pdf.err:
        fname_pdf = plan.PatientId+'_'+planid+'.pdf'
        response = HttpResponse(result.getvalue(), content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename=%s' % fname_pdf
        return response

def csv_export_page(request, planid):
    if planid=='new' or planid=='0':
        return HttpResponseRedirect(reverse(plan_search_page))
    
    plan = get_object_or_404(TREATMENTPLAN, pk=planid)
    
    fname_csv = plan.PatientId+'_'+plan.Filter.Filter.Machine.MachineCode+'_'+planid+'.csv'
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=%s' % fname_csv
    writer = csv.writer(response)

    OutputControlCode = 0
    FractionRad = ''
    if plan.Filter.Filter.Machine.OutputControl == 'MU':
        OutputControlCode = 1
        FractionRad = '%d' % plan.TxTime
    elif plan.Filter.Filter.Machine.OutputControl == 'min':
        OutputControlCode = 0
        FractionRad = '%.2f' % plan.TxTime
    else:
        OutputControlCode = -1
        
    HVLCode = 0
    HVLUnit = plan.Filter.Filter.HVLUnit
    if HVLUnit == 'mm Al':
        HVLCode = 1
    elif HVLUnit == 'mm Cu':
        HVLCode = 2
    elif HVLUnit == 'mm Ti':
        HVLCode = 3
    elif HVLUnit == 'mm Pb':
        HVLCode = 4
    elif HVLUnit == 'mm H2O':
        HVLCode = 5
    
    ConeShapeCode = 0
    ConeBreadth = plan.Cone.Breadth * 10.0
    ConeWidth = plan.Cone.Width * 10.0
    if plan.Cone.Shape == 'Circle':
        ConeShapeCode = 0
        ConeWidth = ''
    elif plan.Cone.Shape == 'Square':
        ConeShapeCode = 1
        ConeWidth = ConeBreadth
    elif plan.Cone.Shape == 'Rectangle':
        ConeShapeCode = 2
    
    CutoutFile = ''
    CutoutRequired = 0
    if plan.CutoutRequired:
        CutoutRequired = 1
    CutoutShape = -1
    if plan.CutoutShape == 'Oval':
        CutoutShape = 0
    elif plan.CutoutShape == 'Rectangle':
        CutoutShape = 1
    
    patient_DOB = ''
    if plan.DOB:
        patient_DOB = datetime.datetime.strftime(plan.DOB,"%Y/%m/%d")
        
        
    EntryTitle = ['PlanId', 'PatientId', 'PatientDOB', 
                   'PatientLastName', 'PatientFirstName', 'PatientMiddleName',
                   'Field', 'Dosimetry', 'FractionRad', 'FractionQty', 'PlanDose',
                   'MachineSN', 'FilterCode', 'kV', 'mA', 'HVLType', 'HVLDim',
                   'ApplicatorCode', 'Shape', 'Breadth', 'Width', 'Length',
                   'CutoutRequired', 'CutoutFile',
                   'CutoutShape', 'CutoutWidth', 'CutoutLength', 'CutoutThinkness',
                   'StandInOut'
                   ]
    CSVEntry = [plan.PatientId+'_'+planid,
                plan.PatientId, patient_DOB,
                plan.LastName, plan.FirstName, plan.MiddleName, 
                
                plan.PlanName,
                OutputControlCode,
                FractionRad, plan.Fractions, plan.TotalDose,
                
                plan.Filter.Filter.Machine.SerialNumber,
                plan.Filter.Filter.FilterCode,
                plan.Filter.Filter.Energy,
                plan.Filter.Filter.Current,
                HVLCode, plan.Filter.Filter.NominalHVL,
                
                plan.Cone.ConeCode, ConeShapeCode, ConeBreadth, ConeWidth,
                plan.Cone.FSD * 10.0, # convert from cm to mm for output
                
                CutoutRequired, CutoutFile, CutoutShape,
                plan.CutoutWidth * 10.0,
                plan.CutoutLength * 10.0,
                plan.CutoutThickness * 10.0,
                
                plan.StandOut * 10.0
                ]

    writer.writerow(EntryTitle)
    writer.writerow(CSVEntry)
    
    ExportCheckSum = True
    if ExportCheckSum:
        # Generate md5checksum
        md5hash = hashlib.md5()
        md5input = ','.join(str(x) for x in CSVEntry)
        md5hash.update(md5input.encode("utf-8"))
        md5output = md5hash.hexdigest()
        
        md5Entry = []
        md5Entry.append(md5output)
        #md5Entry.append(''*(len(CSVEntry)-1))
        writer.writerow(md5Entry)
        #EntryTitle.append('md5checksum')
        #CSVEntry.append(md5output)
    
    return response
