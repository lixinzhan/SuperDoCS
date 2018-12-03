from django.conf.urls import include, url
from django.views.generic import RedirectView
import django.contrib.auth.views as auth_views
from tegmine.views import *


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    url(r'^$', auth_views.login, name='login'),
    url(r'^help/(\w+)/$', help_page, name='help_page'),
    url(r'^help/$',help_page, name='help_page'),
    url(r'^plansearch/$', plan_search_page, name='plan_search_page'),
    url(r'^plan/(\w+)/$', plan_edit_page, name='plan_edit_page'),
    url(r'^plan/$', RedirectView.as_view(url='/plan/new/')),
    url(r'^plan_qa/(\w+)/$', plan_qa_page, name='plan_qa_page'),
    url(r'^plan_qa/$', RedirectView.as_view(url='/plansearch/')),
    url(r'^planstatus/$', RedirectView.as_view(url='/plansearch/')),
    url(r'^planstatus/(\w+)/$',plan_status_page,name='plan_status_page'),

    url(r'^login/$', auth_views.login, name="auth_views.login"),
    url(r'^accounts/login/$', auth_views.login, name='auth_views.login'),
    url(r'^logout/$',logout_page, name='logout_page'),
    url(r'^user/(\w+)/profile/$',profile_page, name='profile_page'),

    url(r'^plan_export/pdf/(\w+)$', pdf_export_page,name='pdf_export_page'),
    url(r'^plan_export/csv/(\w+)$', csv_export_page,name='csv_export_page'),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^commission/', include(admin.site.urls)),
    url('admin/', admin.site.urls),

    # for Language setting view
    url(r'^i18n/', include('django.conf.urls.i18n')), 
]
