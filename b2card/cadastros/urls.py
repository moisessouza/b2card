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
from . import centrocusto
from cadastros.tipohora import TipoHoraList, TipoHoraDetail
from cadastros.centrocusto import CentroCustoList, CentroCustoDetail
from cadastros.centroresultado import CentroResultadoList, CentroResultadoDetail
from cadastros import centroresultado, contagerencial, naturezaoperacao
from cadastros.contagerencial import ContaGerencialList, ContaGerencialDetail
from cadastros.naturezaoperacao import NaturezaOperacaoList, NaturezaOperacaoDetail

app_name='cadastros'

urlpatterns = [
    url(r'^tipohora/$', tipohora.index, name='tipohora'),
    url(r'^centrocusto/$', centrocusto.index, name='centrocusto'),
    url(r'^centroresultado/$', centroresultado.index, name='centroresultado'),
    url(r'^contagerencial/$', contagerencial.index, name='contagerencial'),
    url(r'^naturezaoperacao/$', naturezaoperacao.index, name='naturezaoperacao'),
    url(r'^tipohora/api/list/$', TipoHoraList.as_view()),
    url(r'^tipohora/api/detail/$', TipoHoraDetail.as_view()),
    url(r'^tipohora/api/(?P<tipohora_id>[0-9]+)/$', TipoHoraDetail.as_view()),
    url(r'^centrocusto/api/list/$', CentroCustoList.as_view()),
    url(r'^centrocusto/api/detail/$', CentroCustoDetail.as_view()),
    url(r'^centrocusto/api/(?P<centrocusto_id>[0-9]+)/$', CentroCustoDetail.as_view()),
    url(r'^centroresultado/api/list/$', CentroResultadoList.as_view()),
    url(r'^centroresultado/api/detail/$', CentroResultadoDetail.as_view()),
    url(r'^centroresultado/api/(?P<centroresultado_id>[0-9]+)/$', CentroResultadoDetail.as_view()),
    url(r'^contagerencial/api/list/$', ContaGerencialList.as_view()),
    url(r'^contagerencial/api/detail/$', ContaGerencialDetail.as_view()),
    url(r'^contagerencial/api/(?P<contagerencial_id>[0-9]+)/$', ContaGerencialDetail.as_view()),
    url(r'^naturezaoperacao/api/list/$', NaturezaOperacaoList.as_view()),
    url(r'^naturezaoperacao/api/detail/$', NaturezaOperacaoDetail.as_view()),
    url(r'^naturezaoperacao/api/(?P<naturezaoperacao_id>[0-9]+)/$', NaturezaOperacaoDetail.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)
