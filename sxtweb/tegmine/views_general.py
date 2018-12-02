# Create your views here.
import math
import datetime
import urlparse

from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import RequestContext
from django.contrib.auth import logout, REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render_to_response, get_object_or_404, render
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse

from .models import *
from .forms import *

#
# Page Views
#

@csrf_protect
@never_cache    
def main_page(request, template_name='main_page.html',
          redirect_field_name=REDIRECT_FIELD_NAME,
          authentication_form=AuthenticationForm,
          current_app=None, extra_context=None):
    """
    Displays the login form and handles the login action.
    """
    redirect_to = request.REQUEST.get(redirect_field_name, '')

    if request.method == "POST":
        form = authentication_form(data=request.POST)
        if form.is_valid():
            netloc = urlparse.urlparse(redirect_to)[1]

            # Use default setting if redirect_to is empty
            if not redirect_to:
                redirect_to = settings.LOGIN_REDIRECT_URL
                
            # Security check -- don't allow redirection to a different
            # host.
            elif netloc and netloc != request.get_host():
                redirect_to = settings.LOGIN_REDIRECT_URL
                
            # Okay, security checks complete. Log the user in.
            auth_login(request, form.get_user())
            
            if request.session.test_cookie_worked():
                request.session.delete_test_cookie()

            return HttpResponseRedirect(redirect_to)
    else:
        form = authentication_form(request)
        
    request.session.set_test_cookie()
    
    current_site = get_current_site(request)
    
    context = {
        'site_tab': 'home',
        'form': form,
        redirect_field_name: redirect_to,
        'site': current_site,
        'site_name': current_site.name,
    }
    context.update(extra_context or {})
    #return render_to_response(template_name, context,
    #                          context_instance=RequestContext(request, current_app=current_app))
    return render(request, template_name, context)
        
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
    
