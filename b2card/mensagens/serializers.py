'''
Created on 14 de set de 2016

@author: moi09
'''
from rest_framework import serializers
from mensagens.models import Mensagem

class MensagemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mensagem
        fields = ('id', 'data_criacao', 'texto', 'lido', 'tag')
    
