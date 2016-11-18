from cadastros.centrocusto import CentroCustoList, CentroCustoDetail
from django.conf.urls import url, include
from cadastros import centrocusto

urlpatterns = [
    url(r'^$', centrocusto.index, name='centrocusto'),
    url(r'^api/list/$', CentroCustoList.as_view()),
    url(r'^api/detail/$', CentroCustoDetail.as_view()),
    url(r'^api/(?P<centrocusto_id>[0-9]+)/$', CentroCustoDetail.as_view()),
]
