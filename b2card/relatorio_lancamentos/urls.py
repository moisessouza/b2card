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

app_name='relatorio_lancamentos'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^api/search/$', views.pesquisar_alocacoes_horas),
    url(r'^api/alocarhoras/$', views.alocar_horas),
    url(r'^api/alocarhorasinternas/$', views.alocar_horas_internas),
    url(r'^api/eh_gestor/$', views.eh_gestor),
    url(r'^api/validar_data_hora/(?P<alocacao_id>[0-9]+)/(?P<atividade_id>[0-9]+)/(?P<data_informada>[0-9]+)/(?P<hora_inicio>[0-9:0-9]+)/(?P<hora_fim>[0-9:0-9]+)/$', views.validar_data_hora),
    url(r'^api/verificar_tipo_demanda/(?P<alocacao_id>[0-9]+)/$', views.verificar_tipo_demanda),
    url(r'^api/(?P<alocacao_id>[0-9]+)/excluir/', views.deletar_alocacao)
]

urlpatterns = format_suffix_patterns(urlpatterns)
