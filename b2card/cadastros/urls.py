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
from cadastros import centroresultado, contagerencial, naturezaoperacao, url_centrodecusto
from cadastros.contagerencial import ContaGerencialList, ContaGerencialDetail
from cadastros.naturezaoperacao import NaturezaOperacaoList, NaturezaOperacaoDetail

app_name='cadastros'

urlpatterns = [
    url(r'^tipohora/', include('cadastros.url_tipohora')),
    url(r'^centrocusto/', include('cadastros.url_centrodecusto')),
    url(r'^centroresultado/', include('cadastros.url_centroresultado')),
    url(r'^contagerencial/', include('cadastros.url_contagerencial')),
    url(r'^naturezaoperacao/', include('cadastros.url_naturezaoperacao')),
]

urlpatterns = format_suffix_patterns(urlpatterns)
