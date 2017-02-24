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

app_name='demandas'

urlpatterns = [
    url(r'^$', views.index, name='inicial'),
    url(r'^novo/$', views.novo, name='novo'),
    url(r'^editar/(?P<demanda_id>[0-9]+)/$', views.editar, name='editar'),
    url(r'^api/new/$', views.DemandaDetail.as_view()),
    url(r'^api/(?P<demanda_id>[0-9]+)/$', views.DemandaDetail.as_view()),
    url(r'^api/(?P<demanda_id>[0-9]+)/centroresultadoshora/$', views.buscar_total_horas_custo_resultado_por_demanda),
    url(r'^api/(?P<demanda_id>[0-9]+)/orcamento/totalhoras/$', views.buscar_total_horas_orcamento),
    url(r'^api/(?P<demanda_id>[0-9]+)/orcamento/totalhoras/valorhora/$', views.buscar_total_horas_por_valor_hora),
    url(r'^api/query/$', views.buscar_lista_por_parametro),
    url(r'^api/unidade_administrativa/$', views.buscar_lista_por_unidade_administrativa),
    url(r'^api/profissionalatividade/(?P<atividade_profissional_id>[0-9]+)/possuialocacao/$', views.atividade_profissional_possui_alocacao),
    url(r'^api/atividade/(?P<atividade_id>[0-9]+)/possuialocacao/$', views.atividade_possui_alocacao),
    url(r'^api/texto/(?P<texto>[a-z]+)/$', views.buscar_lista_por_texto),
    url(r'^api/(?P<demanda_id>[0-9]+)/atividades/$', views.buscar_atividades_demanda)
    
]

urlpatterns = format_suffix_patterns(urlpatterns)
