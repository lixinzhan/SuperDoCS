# Create your views here.
import math
import datetime

from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_POST
from django.utils.translation import gettext_lazy as _
from django.urls import reverse

from .models import *
from .forms import *

#
# Page Views
#

@require_POST
@csrf_protect
def logout_page(request):
    logout(request)
    return HttpResponseRedirect('/')

@csrf_protect
@login_required
def profile_page(request, username):
    if not license_is_valid():
        return HttpResponseRedirect(license_page)

    if request.method == 'POST':
        if 'cancel_submit' in request.POST or 'cancel_passwd_submit' in request.POST:
            #return HttpResponseRedirect(reverse(plan_search_page, args=(None))) # not working
            return HttpResponseRedirect('/plansearch/')
        elif 'save_submit' in request.POST:
            uform = UserForm(instance=request.user,data=request.POST,prefix='u')
            if uform.is_valid():
                saved_user=uform.save()
                return HttpResponseRedirect(reverse(profile_page, args=(username,)))
            pform = PasswordForm(request.POST, prefix='p')
        elif 'change_passwd_submit' in request.POST:
            pform = PasswordForm(data=request.POST,user=request.user,prefix='p')
            pform.initial['newpasswd'] = 'here'
            if pform.is_valid():
                pform.save()
                return HttpResponseRedirect(reverse(profile_page, args=(username,)))
            uform = UserForm(request.POST, prefix='u')
        else:
            pform = PasswordForm(user=request.user,prefix='p')
            uform = UserForm(prefix='u')
            uform.initial['first_name'] = request.user.first_name
            uform.initial['last_name'] = request.user.last_name
            uform.initial['email'] = request.user.email
            
    else:
        pform = PasswordForm(user=request.user, prefix='p')
        uform = UserForm(prefix='u')
        uform.initial['first_name'] = request.user.first_name
        uform.initial['last_name'] = request.user.last_name
        uform.initial['email'] = request.user.email
                
    variables = {
        'site_tab': 'settings',
        'uform': uform,
        'pform': pform
    }
    return render(request, 'registration/profile.html', variables)
    
def help_page(request,help_session=''):
    variables = {
        # 'help_session': help_session,
        'site_tab': 'help',
    }
    return render(request, 'help_page.html', variables)
    
