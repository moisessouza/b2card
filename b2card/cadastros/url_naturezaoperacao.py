from django.conf.urls import url, include

from cadastros import naturezaoperacao
from cadastros.naturezaoperacao import NaturezaOperacaoList, NaturezaOperacaoDetail


urlpatterns = [
   url(r'^$', naturezaoperacao.index, name='naturezaoperacao'),
   url(r'^api/list/$', NaturezaOperacaoList.as_view()),
   url(r'^api/detail/$', NaturezaOperacaoDetail.as_view()),
   url(r'^api/(?P<naturezaoperacao_id>[0-9]+)/$', NaturezaOperacaoDetail.as_view())
]