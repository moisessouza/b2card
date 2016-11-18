from cadastros.view_centrocusto import CentroCustoList, CentroCustoDetail
from django.conf.urls import url, include
from cadastros import view_centrocusto

urlpatterns = [
    url(r'^$', view_centrocusto.index, name='centrocusto'),
    url(r'^api/list/$', CentroCustoList.as_view()),
    url(r'^api/detail/$', CentroCustoDetail.as_view()),
    url(r'^api/(?P<centrocusto_id>[0-9]+)/$', CentroCustoDetail.as_view()),
]
