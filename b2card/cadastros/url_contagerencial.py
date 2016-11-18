from django.conf.urls import url, include
from cadastros import contagerencial
from cadastros.contagerencial import ContaGerencialList, ContaGerencialDetail



urlpatterns = [
   url(r'^$', contagerencial.index, name='contagerencial'),
   url(r'^api/list/$', ContaGerencialList.as_view()),
   url(r'^api/detail/$', ContaGerencialDetail.as_view()),
   url(r'^api/(?P<contagerencial_id>[0-9]+)/$', ContaGerencialDetail.as_view()),
]
