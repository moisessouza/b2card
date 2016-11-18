from django.conf.urls import url, include

from cadastros import view_contagerencial
from cadastros.view_contagerencial import ContaGerencialList, ContaGerencialDetail

urlpatterns = [
   url(r'^$', view_contagerencial.index, name='contagerencial'),
   url(r'^api/list/$', ContaGerencialList.as_view()),
   url(r'^api/detail/$', ContaGerencialDetail.as_view()),
   url(r'^api/(?P<contagerencial_id>[0-9]+)/$', ContaGerencialDetail.as_view()),
]
