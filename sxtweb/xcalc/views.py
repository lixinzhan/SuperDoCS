from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from django.http import HttpResponse

import numpy as np

from common.license import *
from .forms import *
from .models import *
# from django.template import loader

# def index(request):
#     context = {
#         'test': "TEST",
#     }
#     return render(request, 'xcalc/index.html', context)


@csrf_protect        
@login_required
def index(request):
    if not license_is_valid(): # don't use LICENSE_VALID
        return HttpResponseRedirect(license_page)

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

    return render(request, 'xcalc/index.html', variables)
