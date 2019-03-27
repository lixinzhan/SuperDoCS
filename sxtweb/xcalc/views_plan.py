# Create your views here.
import math
import datetime
import numpy as np
import urllib.parse

from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.utils.translation import ugettext_lazy as _

from protocols.TG61.CMedWat import CMedWat
from protocols.TG61.BSF_Wat import BSF_Wat
from protocols.TG61.BSF_CloseCone import BSF_CloseCone
from protocols.TG61.BSF_BoneWat import BSF_BoneWat
from protocols.TG61.Mu_WatAir_air import Mu_WatAir_air

from common.errcode import ErrorCode
from xcalib.models import *
from .models import *
from .forms import *
from .curve_fitting import getROF
from .plancalc import *

@csrf_protect        
@login_required
def plan_search_page(request):
    form = PlanSearchForm(request.POST or None)
    planlist = []
    planpage = []
    if request.method == 'POST':
        if 'new_plan_submit' in request.POST and form.is_valid():
            input = form.cleaned_data
            return HttpResponseRedirect(reverse(plan_edit_page, args=('new',)))
        elif 'search_plan_submit' in request.POST and form.is_valid():
            input = form.cleaned_data
            sortkey = input['orderby']
            patientid = input['patientid']
            lastname = input['lastname']
            firstname = input['firstname']
            planname = input['planname']
            planstatus = input['planstatus']
            apprvstatus = input['apprvstatus']
            maxentry = input['maxentry']
            
            request.session['maxentry'] = maxentry
            request.session['planstatus'] = planstatus
            request.session['apprvstatus'] = apprvstatus
            request.session['patientid']= patientid
            request.session['lastname']= lastname
            request.session['firstname']= firstname
            request.session['planname']= planname
            request.session['sortkey']= sortkey
            request.session['has_search'] = True
            
            planlist = TREATMENTPLAN.objects.filter(PatientId__contains=patientid,
                                                LastName__contains=lastname,
                                                FirstName__contains=firstname,
                                                PlanName__contains=planname).order_by(sortkey)
            
            if planstatus != '' and planstatus != 'All':
                planlist = planlist.filter(PlanStatus=planstatus)
            if apprvstatus != '' and apprvstatus != 'All':
                planlist = planlist.filter(ApprvStatus=apprvstatus)
                
            if maxentry=='All':
                num_entry = np.iinfo(np.uint32).max
            else:
                num_entry = np.int(maxentry)
            
            paginator = Paginator(planlist, num_entry)
            try:
                page = int(request.GET.get('page','1'))
            except ValueError:
                page = 1
            try:
                planpage = paginator.page(page)
            except (EmptyPage, InvalidPage):
                planpage = paginator.page(paginator.num_pages)
                
    # variables = RequestContext(request, {
    variables = {
            'site_tab': 'search',
            'form':form,
            #'planlist':planlist,
            'planpage': planpage,
        }

    return render(request, 'plan_search_page.html', variables)

@csrf_protect
@login_required
def plan_status_page(request, planid):    
    access = 'read'
    
    if planid=='new' or planid=='0':
        return HttpResponseRedirect(reverse(plan_search_page))

    plan = get_object_or_404(TREATMENTPLAN, pk=planid)
    
    if request.method=='POST':
        statusform = PlanStatusForm(user=request.user,data=request.POST)
    else:
        statusform = PlanStatusForm(user=request.user,
                                    initial={'planstatus':plan.PlanStatus,'username':request.user})

    if request.method=='POST':
        if 'cancel_submit' in request.POST:
            return HttpResponseRedirect(reverse(plan_edit_page,args=(planid,)))                
        elif 'change_submit' in request.POST:
            if statusform.is_valid():
                status = statusform.cleaned_data
                TREATMENTPLAN.objects.filter(pk=plan.pk).update(PlanStatus=status['planstatus'])
                TREATMENTPLAN.objects.filter(pk=plan.pk).update(StatusChangedBy=status['username'])
                TREATMENTPLAN.objects.filter(pk=plan.pk).update(StatusChangeDateTime=datetime.datetime.now())
                plan.PlanStatus=status['planstatus'] # This is set for correct webpage display.
                return HttpResponseRedirect(reverse(plan_edit_page,args=(planid,)))
        
    variables = {
        'site_tab': 'planning',
        'page_id': 'status',
        'planid': planid,
        'statusform': statusform,
        'access': access,
    }
        
    return render(request, 'plan_status_page.html', variables)

@csrf_protect
@login_required
def plan_qa_page(request, planid):

    access = 'read'
    
    if planid=='new' or planid=='0':
        return HttpResponseRedirect(reverse(plan_search_page))

    plan = get_object_or_404(TREATMENTPLAN, pk=planid)
    authform = AuthForm(user=request.user,data=request.POST or None)
    if request.method=='POST':
        planform = TreatmentPlanForm(instance=plan,data=request.POST)
        if 'planning_submit' in request.POST:
            return HttpResponseRedirect(reverse(plan_edit_page,args=(planid,)))                
        elif 'approval_submit' in request.POST:
            if authform.is_valid():
                auth = authform.cleaned_data
                TREATMENTPLAN.objects.filter(pk=plan.pk).update(ApprvStatus='Approved')
                TREATMENTPLAN.objects.filter(pk=plan.pk).update(ApprovedBy=auth['username'])
                TREATMENTPLAN.objects.filter(pk=plan.pk).update(ApprvDateTime=datetime.datetime.now())
                plan.ApprvStatus='Approved' # This is set for correct webpage display.
        elif 'unapprv_submit' in request.POST:
            if authform.is_valid():
                auth=authform.cleaned_data
                TREATMENTPLAN.objects.filter(pk=plan.pk).update(ApprvStatus='UnApproved')
                TREATMENTPLAN.objects.filter(pk=plan.pk).update(ApprovedBy=auth['username'])
                TREATMENTPLAN.objects.filter(pk=plan.pk).update(ApprvDateTime=datetime.datetime.now())
                plan.ApprvStatus='UnApproved' # This is set for correct webpage display.
    else:
        planform = TreatmentPlanForm(instance=plan)
        
    variables = {
        'site_tab': 'plan_qa',
        'planid': planid,
        'plan': plan,
        'planform': planform,
        'authform': authform,
        'access': access,
    }
        
    return render(request, 'plan_qa_page.html', variables)

@csrf_protect    
@login_required
def plan_edit_page(request, planid):
    if not license_is_valid():
        return HttpResponseRedirect(license_page)

    access = 'edit'
    changeflag = 'none'
    errlist = []
    autoROF = ''
    
    if planid[:3]=='new':
        plan = TREATMENTPLAN()
    else:
        plan = get_object_or_404(TREATMENTPLAN, pk=planid)

    #if 'plan_action_submit' in request.POST:
    #    actionform = PlanActionForm(request.POST)
    #    if actionform.is_valid():
    #        action = actionform.cleaned_data['PlanAction']
    #        if action=='CopyPlan' and planid[:3]=='new':
    #            return HttpResponseRedirect(reverse(plan_edit_page, args=('new',)))
    #        elif action=='CopyPlan':
    #            return HttpResponseRedirect(reverse(plan_edit_page, args=('new_'+planid,)))
    #else:
    #    actionform = PlanActionForm()
        
    if any(cmd_submit in request.POST \
           for cmd_submit in ('cancel_submit','qa_submit','save_submit','calc_submit','copy_submit')):
        if planid[:4]=='new_' and planid[4:]:
            oldplanid = planid[4:]
            oldplan = get_object_or_404(TREATMENTPLAN, pk=oldplanid)                
            copyPlanSetup(plan,oldplan)
            planform = TreatmentPlanForm(instance=plan,data=request.POST)
            planid = 'new'                
        elif planid=='new':
            planform = TreatmentPlanForm(request.POST)
        else:
            autoROF = plan.ROF ########### autoROF ###########
            planform = TreatmentPlanForm(instance=plan,data=request.POST)
           
        if 'cancel_submit' in request.POST:
            return HttpResponseRedirect(reverse(plan_search_page, args=(None)))
        elif planform.is_valid():
            getPlanFormData(plan, planform)
            
            if 'save_submit' in request.POST:
                saved_plan=planform.save()
                if planid=='new':
                    return HttpResponseRedirect(reverse(plan_edit_page,args=(saved_plan.pk,)))
            elif 'qa_submit' in request.POST:
                if planid=='new':
                    saved_plan=planform.save()                
                    return HttpResponseRedirect(reverse(plan_qa_page,args=(saved_plan.pk,)))
                else:
                    return HttpResponseRedirect(reverse(plan_qa_page,args=(planid,)))                
            #elif 'copy_submit' in request.POST:
            #    return HttpResponseRedirect(reverse(plan_edit_page, args=('new_'+str(plan.pk),)))
            elif 'calc_submit' in request.POST:
                calcTxPlan(plan, errlist)
                changeflag = 'newcalc'
                if planid=='new':
                    plan.PlanStatus = 'Active'
                    plan.StatusChangedBy = 'nobody'
                    plan.StatusChangeDateTime = datetime.datetime.now
                    plan.ApprvStatus = 'NotApproved'
                    plan.ApprovedBy = 'nobody'
                    plan.ApprvDateTime = datetime.datetime.now
    else: # not request.POST
        if planid[:4]=='new_' and planid[4:]:
            oldplanid = planid[4:]
            oldplan = get_object_or_404(TREATMENTPLAN, pk=oldplanid)                
            copyPlanSetup(plan,oldplan)
            planform = TreatmentPlanForm(instance=plan)
            planid = 'new'                
        elif planid=='new':
            planform = TreatmentPlanForm()
        else:
            autoROF = plan.ROF ########### autoROF ###########
            planform = TreatmentPlanForm(instance=plan)
            
    try:
        if errlist[0][:3]=='ERR':
            error = errlist[0]
        else:
            error = ErrorCode[errlist[0]] # django not supporting ugettext_lazy concatenate yet.
    except: # usually out of index boundary, which means no error raised.
        error = ''
        
    variables = {
        'site_tab': 'planning',
        'planid': planid,
        'plan': plan,
        'planform': planform,
        #'actionform': actionform,
        'changeflag': changeflag,
        'access': access,
        'error': error,
        'autoROF': autoROF
    }
    return render(request, 'plan_edit_page.html', variables)
