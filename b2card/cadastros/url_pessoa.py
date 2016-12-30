from django.conf.urls import url, include
from cadastros import view_pessoa



urlpatterns = [
    url(r'^$', view_pessoa.index, name='pessoa'),
    url(r'^novo/$', view_pessoa.novo, name="pessoa_novo")
]