from django.conf.urls import url
from cadastros import view_naturezademanda

urlpatterns = [
    url(r'^$', view_naturezademanda.index, name='naturezademanda'),
    url(r'^api/list/$', view_naturezademanda.NaturezaDemandaList.as_view()),
    url(r'^api/detail/$', view_naturezademanda.NaturezaDemandaDetail.as_view()),
    url(r'^api/(?P<naturezademanda_id>[0-9]+)/$', view_naturezademanda.NaturezaDemandaDetail.as_view())
]
