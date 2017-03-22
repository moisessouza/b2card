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
    url(r'^contasreceber/$', views.contas_receber_prevista, name="contasreceber"),
    url(r'^api/parcela/new/$', views.ParcelaList.as_view()),
    url(r'^api/parcela/demanda/(?P<demanda_id>[0-9]+)/$', views.buscar_parcela_por_demanda_id),
    url(r'^api/parcela/fase/tipohora/(?P<demanda_id>[0-9]+)/$', views.buscar_tipo_hora_por_fases),
    url(r'^api/contasreceber/search/$', views.search_contas_receber),
    url(r'^api/orcamento/(?P<demanda_id>[0-9]+)/$', views.buscar_orcamento_demanda_id),
    url(r'^api/buscarpacoteitens/(?P<cliente_id>[0-9]+)/$', views.buscar_pacote_itens_cliente),
    url(r'^api/pacoteitens/$', views.criar_pacote_itens),
    url(r'^api/enviaraprovacao/$', views.enviar_para_aprovacao),
    url(r'^api/enviarfaturamento/$', views.enviar_para_faturamento),
    url(r'^gerar_arquivo_faturamento/(?P<demanda_id>[0-9]+)/$', views.gerar_arquivo_faturamento),
    url(r'^gerar_arquivo_faturamento_comercial/(?P<demanda_id>[0-9]+)/$', views.gerar_arquivo_faturamento_comercial),
    url(r'^gerar_arquivo_aprovacao/(?P<pacote_itens_id>[0-9]+)/$', views.gerar_arquivo_aprovacao),
    url(r'^api/lotedespesas/new/$', views.gerar_lote_despesas),
    url(r'^api/lotedespesas/abertos/(?P<demanda_id>[0-9]+)/$', views.buscar_lote_despesas_abertos),
    url(r'^relatorio/relatorio_despesas/(?P<lote_despesa_id>[0-9]+)/$', views.relatorio_despesas)
]

urlpatterns = format_suffix_patterns(urlpatterns)
