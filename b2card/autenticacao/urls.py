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

app_name='autenticacao'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^falha/$', views.falha, name='falha'),
    url(r'^alterar/$', views.alterar_senha, name='alterar_senha'),
    url(r'^executar_alteracao/$', views.executar_alteracao, name='executar_alteracao'),
    url(r'^login/$', views.executar, name='login'),
    url(r'^logout/$', views.logout_view, name='logout_view'),
    url(r'^not_permitted/$', views.not_permitted, name='not_permitted'),
    url(r'^api/permissoesaba/$', views.verificar_permissoes_abas)
]

urlpatterns = format_suffix_patterns(urlpatterns)
