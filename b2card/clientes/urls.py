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
    url(r'^(?P<cliente_id>[0-9]+)/$', views.editar, name='editar'),
    url(r'^api/list/$', views.ClienteList.as_view()),
    url(r'^api/new', views.ClienteDetail.as_view()),
    url(r'^api/cliente/(?P<cliente_id>[0-9]+)/valorhora/$', views.buscar_valor_hora_cliente),
    url(r'^api/cliente/(?P<cliente_id>[0-9]+)/centroresultado/$', views.buscar_centro_resultados_cliente),
    url(r'^api/(?P<cliente_id>[0-9]+)/$', views.ClienteDetail.as_view()),
    url(r'^api/valorhora/(?P<tipo_valor_hora_id>[0-9]+)/$', views.TipoValorHoraDetail.as_view()),
    url(r'^api/centroresultado/(?P<centro_resultado_id>[0-9]+)/$', views.CentroResultadoDetail.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)
