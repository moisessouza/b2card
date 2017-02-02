from django.conf.urls import url
from cadastros import view_fase

urlpatterns = [
    url(r'^$', view_fase.index, name='fase'),
    url(r'^api/list/$', view_fase.FaseList.as_view()),
    url(r'^api/detail/$', view_fase.FaseDetail.as_view()),
    url(r'^api/(?P<fase_id>[0-9]+)/$', view_fase.FaseDetail.as_view())
]
