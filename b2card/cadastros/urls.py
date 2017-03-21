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

app_name='cadastros'

urlpatterns = [
    url(r'^tipohora/', include('cadastros.url_tipohora')),
    url(r'^centrocusto/', include('cadastros.url_centrodecusto')),
    url(r'^centroresultado/', include('cadastros.url_centroresultado')),
    url(r'^contagerencial/', include('cadastros.url_contagerencial')),
    url(r'^naturezaoperacao/', include('cadastros.url_naturezaoperacao')),
    url(r'^valorhora/', include('cadastros.url_valorhora')),
    url(r'^unidadeadministrativa/', include('cadastros.url_unidadeadministrativa')),
    url(r'^pessoa/', include('cadastros.url_pessoa')),
    url(r'^fase/', include('cadastros.url_fase')),
    url(r'^naturezademanda/', include('cadastros.url_naturezademanda')),
    url(r'^tipoalocacao/', include('cadastros.url_tipoalocacao')),
    url(r'^tipodespesa/', include('cadastros.url_tipodespesa')),
]

urlpatterns = format_suffix_patterns(urlpatterns)
