"""sxtweb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LoginView

# admin.site.logged_out_template = 'registration/logged_out.html'
# admin.autodiscover()

urlpatterns = [
    path('login/',LoginView.as_view(template_name='admin/login.html',
            extra_context={'site_header': 'SuperDoCS Login',
                'next': '/admin/'})),
    path('admin/',  admin.site.urls),
    path('xcalc/',  include('xcalc.urls')),
    path('xcalib/', include('xcalib.urls')),
    path('resources/', include('resources.urls')),
]
