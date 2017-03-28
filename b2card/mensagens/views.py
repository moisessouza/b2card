from django.shortcuts import render
from rest_framework.decorators import api_view
from mensagens.models import Mensagem
from rest_framework.response import Response
from mensagens.serializers import MensagemSerializer
from utils.utils import serializar_data

# Create your views here.

@api_view(['GET'])
def list(request, format=None):
    mensagens = Mensagem.objects.filter(pessoa_fisica__prestador__usuario__id = request.user.id, lido=False).order_by('-data_criacao')
    list = MensagemSerializer(mensagens, many=True).data
    
    for i in list:
        i['data_criacao'] = serializar_data(i['data_criacao'])
    
    return Response(list)

@api_view(['GET'])
def marcar_como_lido(request, mensagem_id, format=None):
    mensagem = Mensagem.objects.get(pk=mensagem_id, pessoa_fisica__prestador__usuario__id = request.user.id)
    mensagem.lido = True
    mensagem.save();
    
    mensagem = MensagemSerializer(mensagem).data
    mensagem['data_criacao'] = serializar_data(mensagem['data_criacao'])
    
    return Response(mensagem)
    