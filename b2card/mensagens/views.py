# -*- coding: utf-8 -*-
from django.shortcuts import render
from rest_framework.decorators import api_view
from mensagens.models import Mensagem, Responsavel
from rest_framework.response import Response
from mensagens.serializers import MensagemSerializer, ResponsavelSerializer
from utils.utils import serializar_data, converter_string_para_data,\
    formatar_data
from cadastros.models import PessoaFisica, Pessoa, Prestador
from datetime import datetime
from rest_framework.views import APIView

from django.db.models import Q

# Create your views here.

def index(request):
    return render(request, 'mensagens/index.html')

def enviar_mensagem(request):
    return render(request, 'mensagens/enviar_mensagem.html')

@api_view(['GET'])
def list(request, format=None):
    mensagens = Mensagem.objects.filter(pessoa_fisica__prestador__usuario__id = request.user.id, lido=False, data_criacao__lte = datetime.now()).order_by('-data_criacao')
    list = MensagemSerializer(mensagens, many=True).data
    
    for i in list:
        i['data_criacao'] = serializar_data(i['data_criacao'])
    
    return Response(list)

@api_view(['GET'])
def marcar_como_lido(request, mensagem_id, format=None):
    mensagem = Mensagem.objects.get(pk=mensagem_id, pessoa_fisica__prestador__usuario__id = request.user.id)
    mensagem.delete()
    
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

@api_view(['POST'])
def enviar_mensagem_destinatario(request, format=None):
    
    if request.user.is_superuser:
        origem = "Super usuário"
    else:
        origem = Pessoa.objects.filter(pessoafisica__prestador__usuario__id = request.user.id)[0]
        origem = origem.nome_razao_social
    
    destino = None
    if 'destino' in request.data and request.data['destino']:
        if 'id' in request.data['destino']:
            destino = PessoaFisica.objects.get(pk=request.data['destino']['id'])
    
    mensagem = Mensagem()
    mensagem.origem = origem
    mensagem.pessoa_fisica = destino
    mensagem.tag= 'M'
    mensagem.texto = request.data['mensagem']
    mensagem.data_criacao = datetime.now().date()
    mensagem.save()
    
    return Response(MensagemSerializer(mensagem).data)

def tarefas(request):
    return render(request, 'mensagens/tarefa/index.html')

class TarefaList(APIView):
    def get(self, request, format=None):
        
        mensagem = Mensagem.objects.filter(tag='T').order_by('data_criacao')
        
        if not request.user.is_superuser:
            eh_gestor = Prestador.objects.filter(Q(data_fim__isnull=True) | Q(data_fim__gte = datetime.now()), Q(cargo__gestor=True), Q(usuario__id = request.user.id))
    
            if len(eh_gestor) <= 0:
                mensagem = mensagem.filter(pessoa_fisica__prestador__usuario__id = request.user.id) 
                
        for i in mensagem:
            i.data_criacao = formatar_data(i.data_criacao)
        
        serializer = MensagemSerializer(mensagem, many=True)
        return Response(serializer.data)
    
class TarefaDetail(APIView):
    def post(self, request, format=None):
        
        if 'origem' not in request.data:
            if request.user.is_superuser:
                origem = "Super usuário"
            else:
                origem = Pessoa.objects.filter(pessoafisica__prestador__usuario__id = request.user.id)[0]
                origem = origem.nome_razao_social
        else:
            origem = request.data['origem']
        
        destino = None
        if 'pessoa_fisica' in request.data and request.data['pessoa_fisica']:
            if 'id' in request.data['pessoa_fisica']:
                destino = PessoaFisica.objects.get(pk=request.data['pessoa_fisica']['id'])
            del request.data['pessoa_fisica']
        else:
            destino = PessoaFisica.objects.filter(prestador__usuario__id = request.user.id)[0]
            
        if 'data_texto' in request.data:
            del request.data['data_texto']
        
        mensagem = Mensagem(**request.data)
        mensagem.origem = origem
        mensagem.pessoa_fisica = destino
        mensagem.data_criacao =converter_string_para_data(request.data['data_criacao'])
        mensagem.tag='T'
        mensagem.save()
                
        serializer = MensagemSerializer(mensagem)
        return Response(serializer.data)
    
    def delete(self, request, mensagem_id, format=None):
        mensagem = Mensagem.objects.get(pk=mensagem_id)
        mensagem.delete()
        serializer = MensagemSerializer(mensagem)
        return Response(serializer.data)   
