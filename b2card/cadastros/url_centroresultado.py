from django.conf.urls import url, include

from cadastros import centroresultado
from cadastros.centroresultado import CentroResultadoList, CentroResultadoDetail


urlpatterns = [
    url(r'^$', centroresultado.index, name='centroresultado'),
    url(r'^api/list/$', CentroResultadoList.as_view()),
    url(r'^api/detail/$', CentroResultadoDetail.as_view()),
    url(r'^api/(?P<centroresultado_id>[0-9]+)/$', CentroResultadoDetail.as_view()),
]
