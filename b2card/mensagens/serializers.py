'''
Created on 14 de set de 2016

@author: moi09
'''
from rest_framework import serializers
from mensagens.models import Mensagem, Responsavel
from cadastros.serializers_pessoa import PessoaFisicaSerializer,\
    PessoaFisicaComPessoaSerializer

class MensagemSerializer(serializers.ModelSerializer):
    pessoa_fisica = PessoaFisicaComPessoaSerializer()
    class Meta:
        model = Mensagem
        fields = ('id', 'pessoa_fisica', 'data_criacao', 'origem', 'texto', 'lido', 'tag')
    
class ResponsavelSerializer(serializers.ModelSerializer):
    pessoa_fisica = PessoaFisicaSerializer()
    class Meta:
        model = Responsavel
        fields = ('id', 'pessoa_fisica', 'tag', 'ativo')