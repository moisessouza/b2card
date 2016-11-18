from django.conf.urls import url, include

from cadastros import view_tipohora
from cadastros.view_tipohora import TipoHoraList, TipoHoraDetail

urlpatterns = [
    url(r'^$', view_tipohora.index, name='tipohora'),
    url(r'^api/list/$', TipoHoraList.as_view()),
    url(r'^api/detail/$', TipoHoraDetail.as_view()),
    url(r'^api/(?P<tipohora_id>[0-9]+)/$', TipoHoraDetail.as_view())
]
