from django.conf.urls import url
from cadastros import view_tipodespesa

urlpatterns = [
    url(r'^$', view_tipodespesa.index, name='tipodespesa'),
    url(r'^api/list/$', view_tipodespesa.TipoDespesaList.as_view()),
    url(r'^api/detail/$', view_tipodespesa.TipoDespesaDetail.as_view()),
    url(r'^api/(?P<tipodespesa_id>[0-9]+)/$', view_tipodespesa.TipoDespesaDetail.as_view())
]
