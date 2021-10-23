from django.conf.urls import include, url
from django.urls import re_path
from django.views.generic import RedirectView
import django.contrib.auth.views as auth_views
from xcalc.views import *


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    re_path(r'^$', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    re_path(r'^help/(\w+)/$', help_page, name='help_page'),
    re_path(r'^help/$',help_page, name='help_page'),
    re_path(r'^plansearch/$', plan_search_page, name='plan_search_page'),
    re_path(r'^plan/(\w+)/$', plan_edit_page, name='plan_edit_page'),
    re_path(r'^plan/$', RedirectView.as_view(url='/plan/new/')),
    re_path(r'^plan_qa/(\w+)/$', plan_qa_page, name='plan_qa_page'),
    re_path(r'^plan_qa/$', RedirectView.as_view(url='/plansearch/')),
    re_path(r'^planstatus/$', RedirectView.as_view(url='/plansearch/')),
    re_path(r'^planstatus/(\w+)/$',plan_status_page,name='plan_status_page'),

    re_path(r'^login/$', auth_views.LoginView.as_view()), #name="auth_views.login"),
    re_path(r'^accounts/login/$', auth_views.LoginView.as_view()), #name='auth_views.login'),
    re_path(r'^logout/$',logout_page, name='logout_page'),
    re_path(r'^user/(\w+)/profile/$',profile_page, name='profile_page'),

    re_path(r'^plan_export/pdf/(\w+)$', pdf_export_page,name='pdf_export_page'),
    re_path(r'^plan_export/csv/(\w+)$', csv_export_page,name='csv_export_page'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # re_path(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # re_path(r'^commission/', include(admin.site.urls)),
    re_path('admin/', admin.site.urls),

    # for Language setting view
    re_path(r'^i18n/', include('django.conf.urls.i18n')), 
]
