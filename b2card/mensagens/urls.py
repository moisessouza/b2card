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

app_name='mensagens'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^enviar_mensagem/$', views.enviar_mensagem, name='enviar_mensagem'),
    url(r'^api/responsaveis/$', views.buscar_responsaveis),
    url(r'^api/list/$', views.list),
    url(r'^api/marcarcomolido/(?P<mensagem_id>[0-9]+)/$', views.marcar_como_lido),
    url(r'^api/gravarresponsaveis/$', views.gravar_responsaveis),
    url(r'^api/deletarresponsaveis/(?P<responsavel_id>[0-9]+)/$', views.deletar_responsavel),
    url(r'^api/enviar_mensagem/$', views.enviar_mensagem_destinatario),
    #Tarefa
    url(r'^tarefa/$', views.tarefas, name='tarefas'),
    url(r'^tarefa/api/list/$', views.TarefaList.as_view()),
    url(r'^tarefa/api/detail/$', views.TarefaDetail.as_view()),
    url(r'^tarefa/api/(?P<mensagem_id>[0-9]+)/$', views.TarefaDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
