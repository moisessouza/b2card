from django.conf.urls import url, include
from . import view_unidadeadministrativa

urlpatterns = [
    url(r'^$', view_unidadeadministrativa.index, name='unidadeadministrativa'),
    url(r'^api/list/$', view_unidadeadministrativa.UnidadeAdministrativaList.as_view()),
    url(r'^api/detail/$', view_unidadeadministrativa.UnidadeAdministrativaDetail.as_view()),
    url(r'^api/(?P<unidade_administrativa_id>[0-9]+)/$', view_unidadeadministrativa.UnidadeAdministrativaDetail.as_view()),
]
