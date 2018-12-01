from django.urls import path
from . import views
from . import apps

app_name = apps.XcalcConfig.name

urlpatterns = [
    path('', views.index, name='index'),
]
