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
from . import tipohora
from cadastros.tipohora import TipoHoraList, TipoHoraDetail

app_name='cadastros'

urlpatterns = [
    url(r'^tipohora/$', tipohora.index, name='tipohora'),
    url(r'^tipohora/api/list/$', TipoHoraList.as_view()),
    url(r'^tipohora/api/detail/$', TipoHoraDetail.as_view()),
     url(r'^tipohora/api/(?P<tipohora_id>[0-9]+)/$', TipoHoraDetail.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)
