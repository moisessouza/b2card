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

app_name='faturamento'

urlpatterns = [
    url(r'^contasreceber', views.contas_receber_prevista, name="contasreceber"),
    url(r'^api/parcela/new/$', views.ParcelaList.as_view()),
    url(r'^api/parcela/demanda/(?P<demanda_id>[0-9]+)/$', views.buscar_parcela_por_demanda_id),
    url(r'^api/parcela/fase/tipohora/(?P<demanda_id>[0-9]+)/$', views.buscar_tipo_hora_por_fases),
    url(r'^api/contasreceber/search/$', views.search_contas_receber),
    url(r'^api/orcamento/(?P<demanda_id>[0-9]+)/$', views.buscar_orcamento_demanda_id)
]

urlpatterns = format_suffix_patterns(urlpatterns)
