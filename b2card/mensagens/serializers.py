'''
Created on 14 de set de 2016

@author: moi09
'''
from rest_framework import serializers
from mensagens.models import Mensagem, Responsavel
from cadastros.serializers_pessoa import PessoaFisicaSerializer

class MensagemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mensagem
        fields = ('id', 'data_criacao', 'origem', 'texto', 'lido', 'tag')
    
class ResponsavelSerializer(serializers.ModelSerializer):
    pessoa_fisica = PessoaFisicaSerializer()
    class Meta:
        model = Responsavel
        fields = ('id', 'pessoa_fisica', 'tag', 'ativo')