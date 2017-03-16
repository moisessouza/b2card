from django.conf.urls import url, include
from cadastros import view_pessoa



urlpatterns = [
    url(r'^$', view_pessoa.index, name='pessoa'),
    url(r'^novo/$', view_pessoa.novo, name="pessoa_novo"),
    url(r'^editar/(?P<pessoa_id>[0-9]+)/$', view_pessoa.editar),
    url(r'^api/new/$', view_pessoa.PessoaDetail.as_view()),
    url(r'^api/(?P<pessoa_id>[0-9]+)/$', view_pessoa.PessoaDetail.as_view()),
    url(r'^api/list/$', view_pessoa.PessoaList.as_view()),
    url(r'^api/pessoajuridica/list/$', view_pessoa.PessoaJuridicaList.as_view()),
    url(r'^api/pessoafisica/list/$', view_pessoa.PessoaFisicaList.as_view()),
    url(r'^api/pessoafisica/(?P<texto>.*)/$', view_pessoa.buscar_pessoas_por_nome),
    url(r'^api/gestores/$', view_pessoa.buscar_gestores),
    url(r'^api/pessoajuridica/uploadarquivo/(?P<pessoa_juridica_id>[0-9]+)/$', view_pessoa.upload_arquivo),
    url(r'^api/pessoajuridica/removerarquivo/(?P<pessoa_juridica_id>[0-9]+)/$', view_pessoa.remover_arquivo),
    url(r'^api/pessoajuridica/baixararquivo/(?P<pessoa_juridica_id>[0-9]+)/$', view_pessoa.baixar_arquivo),
    url(r'^api/pessoajuridica/clientes/$', view_pessoa.buscar_pessoa_juridica_clientes),
]