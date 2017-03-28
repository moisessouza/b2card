from django.shortcuts import render
from rest_framework.decorators import api_view
from mensagens.models import Mensagem, Responsavel
from rest_framework.response import Response
from mensagens.serializers import MensagemSerializer, ResponsavelSerializer
from utils.utils import serializar_data
from cadastros.models import PessoaFisica

# Create your views here.

def index(request):
    return render(request, 'mensagens/index.html')

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


@api_view(['GET'])
def buscar_responsaveis(request, format=None):
    responsaveis = Responsavel.objects.all()
    return Response(ResponsavelSerializer(responsaveis, many=True).data)

@api_view(['POST'])
def gravar_responsaveis(request, format=None):

    lista_responsavel = []

    for i in request.data:
        
        pessoa_fisica = None
        if 'pessoa_fisica' in i:
            if 'id' in i['pessoa_fisica'] and i['pessoa_fisica']['id']:
                pessoa_fisica = PessoaFisica.objects.get(pk=i['pessoa_fisica']['id'])
            del i['pessoa_fisica']
            
        responsavel = Responsavel(**i)
        responsavel.pessoa_fisica = pessoa_fisica
        responsavel.save()
        lista_responsavel.append(responsavel)
        
    return Response(ResponsavelSerializer(lista_responsavel, many=True).data)

@api_view(['GET'])
def deletar_responsavel(request, responsavel_id, format=None):
    
    responsavel = Responsavel.objects.get(pk=responsavel_id)
    responsavel.delete()
    
    return Response(ResponsavelSerializer(responsavel).data)