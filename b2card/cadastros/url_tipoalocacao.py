from django.conf.urls import url
from cadastros import view_tipoalocacao

urlpatterns = [
    url(r'^$', view_tipoalocacao.index, name='tipoalocacao'),
    url(r'^api/list/$', view_tipoalocacao.TipoAlocacaoList.as_view()),
    url(r'^api/detail/$', view_tipoalocacao.TipoAlocacaoDetail.as_view()),
    url(r'^api/(?P<tipoalocacao_id>[0-9]+)/$', view_tipoalocacao.TipoAlocacaoDetail.as_view())
]
