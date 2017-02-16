# -*- coding: utf-8 -*-
from django.shortcuts import render
from rest_framework.decorators import api_view
from demandas.models import Demanda, FaseAtividade
from django.db.models import Q
from cadastros.models import PessoaJuridica
from cadastros.serializers_pessoa import PessoaJuridicaSerializer

from rest_framework.response import Response
from demandas.serializers import DemandaSerializer, DemandaInicialSerializer
from demandas.views import serializar_fase_atividade

# Create your views here.
def index(request):
    return render(request, 'gestor/index.html')

@api_view(['POST'])
def buscar_clientes_demandas(request, format=None):
    
    clientes = PessoaJuridica.objects.filter(Q(demanda__responsavel__prestador__usuario__id=request.user.id) | Q(demanda__faseatividade__responsavel__prestador__usuario__id=request.user.id)).distinct()
    
    list_status = []
    if request.data:
        for k in request.data:
            if request.data[k]:
                list_status.append(k)
    
    cliente_list = []
    
    for i in clientes:
        cliente = PessoaJuridicaSerializer(i).data

        if list_status:
            demandas = Demanda.objects.filter(status_demanda__in=list_status).filter(Q(cliente = i), Q(responsavel__prestador__usuario__id=request.user.id)).order_by('-id')
        else:
            demandas = Demanda.objects.filter(Q(cliente = i), Q(responsavel__prestador__usuario__id=request.user.id)).order_by('-id')

        demanda_list = []
        
        for d in demandas:
            demanda = DemandaInicialSerializer(d).data
            demanda_list.append(demanda)
        
        if list_status:
            demandas = Demanda.objects.filter(status_demanda__in=list_status).filter(cliente = i, faseatividade__responsavel__prestador__usuario__id=request.user.id).exclude(id__in=[d.id for d in demandas]).distinct().order_by('-id')
        else:
            demandas = Demanda.objects.filter(cliente = i, faseatividade__responsavel__prestador__usuario__id=request.user.id).exclude(id__in=[d.id for d in demandas]).distinct().order_by('-id')
            
        
        for d in demandas:
            demanda_dict = DemandaInicialSerializer(d).data
            demanda_list.append(demanda_dict)
            
        cliente['demandas'] = demanda_list
        cliente_list.append(cliente)
        
        
    return Response(cliente_list)


@api_view(['GET'])
def buscar_atividades_demanda(request, demanda_id, format=None):
    
    fase_atividade_list = []
    
    fase_atividades = FaseAtividade.objects.filter(demanda__id = demanda_id, responsavel__prestador__usuario__id=request.user.id)
    if fase_atividades:
        fase_atividade_list.extend(serializar_fase_atividade(fase_atividades))
    
    fase_atividades = FaseAtividade.objects.filter(demanda__id = demanda_id, demanda__responsavel__prestador__usuario__id= request.user.id).exclude(id__in=[f.id for f in fase_atividades])
    if fase_atividades:
        fase_atividade_list.extend(serializar_fase_atividade(fase_atividades))
    
    return Response(fase_atividade_list)