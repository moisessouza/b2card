from cadastros import view_valorhora
from django.conf.urls import url, include
from cadastros.view_valorhora import ValorHoraDetail

urlpatterns = [
    url(r'^$', view_valorhora.index, name='valorhora'),
    url(r'^novo/$', view_valorhora.novo, name='novo_valor_hora'),
    url(r'^(?P<valorhora_id>[0-9]+)/$', view_valorhora.editar, name='editar_valor_hora'),
    url(r'^api/detail/$', ValorHoraDetail.as_view()),
    url(r'^api/(?P<valorhora_id>[0-9]+)/$', ValorHoraDetail.as_view()),
    url(r'^api/cliente/(?P<cliente_id>[0-9]+)/(?P<data>[0-9]+)/$', view_valorhora.buscar_valor_hora_por_cliente),
    url(r'^api/b2card/(?P<data>[0-9]+)/$', view_valorhora.buscar_valor_hora_b2card),
    url(r'^api/b2cardtx/(?P<data>[0-9]+)/$', view_valorhora.buscar_valor_imposto_custoadmin_b2card),
    url(r'^api/$', view_valorhora.buscar_valor_horas),
]