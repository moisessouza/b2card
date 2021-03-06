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

app_name='recursos'

urlpatterns = [
    url(r'^api/cargo/list/$', views.CargoList.as_view()),
    url(r'^api/cargo/new/$', views.CargoDetail.as_view()),
    url(r'^api/cargo/(?P<cargo_id>[0-9]+)/$', views.CargoDetail.as_view()),
    url(r'^api/usuarios/(?P<prestador_id>[0-9]+)/$', views.buscar_usuario_prestador),
    url(r'^api/usuarios/$', views.buscar_usuarios_nao_usados)
]

urlpatterns = format_suffix_patterns(urlpatterns)
