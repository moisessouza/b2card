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

app_name='inicial'

urlpatterns = [
    url(r'^$', views.index, name='inicial'),
    url(r'^api/atividadesprofissional/$', views.buscar_atividades_usuario),
    url(r'^api/alocacao/$', views.alocar_horas),
    url(r'^api/ultimaalocacao/(?P<atividade_profissional_id>[0-9]+)/$', views.buscar_ultima_alocacao),
    url(r'^api/atividadesprofissional/(?P<atividade_id>[0-9]+)/$', views.buscar_atividade_profissional_por_atividade),
    url(r'^api/atividadesprofissional/demanda/(?P<demanda_id>[0-9]+)/$', views.buscar_atividades_demanda),
    url(r'^api/atividadesinternas/$', views.buscar_atividades_internas),
    url(r'^api/atividadesinternas/demanda/(?P<demanda_id>[0-9]+)/$', views.buscar_atividades_demanda_interna),
    url(r'^api/alocacaointerna/$', views.alocar_horas_internas),
    url(r'^api/validar_data_hora/(?P<data_informada>[0-9]+)/(?P<hora_inicio>[0-9:0-9]+)/(?P<hora_fim>[0-9:0-9]+)/$', views.validar_data_hora),
]

urlpatterns = format_suffix_patterns(urlpatterns)
