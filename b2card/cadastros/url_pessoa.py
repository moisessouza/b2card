from django.conf.urls import url, include
from cadastros import view_pessoa



urlpatterns = [
    url(r'^$', view_pessoa.index, name='pessoa'),
    url(r'^novo/$', view_pessoa.novo, name="pessoa_novo"),
    url(r'^editar/(?P<pessoa_id>[0-9]+)/$', view_pessoa.editar),
    url(r'^api/new/$', view_pessoa.PessoaDetail.as_view()),
    url(r'^api/(?P<pessoa_id>[0-9]+)/$', view_pessoa.PessoaDetail.as_view()),
    url(r'^api/list/$', view_pessoa.PessoaList.as_view()),
]