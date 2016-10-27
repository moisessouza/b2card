"""getbasket URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from rest_framework import routers, serializers, viewsets
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

app_name='clientes'

urlpatterns = [
    url(r'^$', views.index, name='inicial'),
    url(r'^novo/$', views.novo, name='novo'),
    url(r'^gravar/$', views.executar, name='gravar'),
    url(r'^(?P<cliente_id>[0-9]+)/$', views.editar, name='editar')
]

urlpatterns = format_suffix_patterns(urlpatterns)
