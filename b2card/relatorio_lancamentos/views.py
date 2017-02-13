# -*- coding: utf-8 -*-
import datetime

from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Q

from cadastros.models import TipoAlocacao, Prestador
from demandas.models import AlocacaoHoras, AtividadeProfissional, Atividade, \
    FaseAtividade, Demanda
from demandas.serializers import AlocacaoHorasSerializer, \
    RelatorioAlocacaoHorasSerializer, AtividadeProfissionalSerializer
from utils.utils import converter_string_para_data, formatar_data,\
    serializar_data


# Create your views here.
def index(request):
    return render(request, 'relatorio_lancamentos/index.html')


@api_view(['POST'])
def pesquisar_alocacoes_horas(request, format=None):
    
    periodo = request.data['periodo']
    periodo = converter_string_para_data(periodo)
    
    alocacao_horas = AlocacaoHoras.objects.filter(data_informada__month=periodo.month, data_informada__year=periodo.year)
    
    if 'profissional_id' in request.data and request.data['profissional_id']:
        alocacao_horas = alocacao_horas.filter(atividade_profissional__pessoa_fisica__id=request.data['profissional_id'])
        
    if 'cliente_id' in request.data and request.data['cliente_id']:
        alocacao_horas = alocacao_horas.filter(atividade_profissional__atividade__fase_atividade__demanda__cliente__id=request.data['cliente_id'])
        
    if 'status_demanda' in request.data and request.data['status_demanda']:
        alocacao_horas = alocacao_horas.filter(atividade_profissional__atividade__fase_atividade__demanda__status_demanda=request.data['status_demanda'])
        
    if 'demanda' in request.data and request.data['demanda']:
        alocacao_horas = alocacao_horas.filter(atividade_profissional__atividade__fase_atividade__demanda__id=request.data['demanda']['id'])
        
    if not request.user.is_superuser:
        eh_gestor = Prestador.objects.filter(Q(data_fim__isnull=True) | Q(data_fim__gte = datetime.datetime.now()), Q(cargo__gestor=True), Q(usuario__id = request.user.id))
    
        if len(eh_gestor) <= 0:
            alocacao_horas = alocacao_horas.filter(atividade_profissional__pessoa_fisica__prestador__usuario__id = request.user.id)
        
    alocacao_hora_list = RelatorioAlocacaoHorasSerializer(alocacao_horas, many=True).data
    
    for i in alocacao_hora_list:
        i['data_alocacao'] = serializar_data(i['data_alocacao'])
        
    return Response(alocacao_hora_list)

@api_view(['GET'])
def eh_gestor(request, format=None):
    if request.user.is_superuser:
        return Response({'gestor': True})
    
    if not request.user.is_superuser:
        eh_gestor = Prestador.objects.filter(Q(data_fim__isnull=True) | Q(data_fim__gte = datetime.datetime.now()), Q(cargo__gestor=True), Q(usuario__id = request.user.id))
        if len(eh_gestor) > 0:
            return Response({'gestor':True})
        
    return Response({'gestor':False})

@api_view(['POST'])
def alocar_horas(request, format=None):
    
    if 'alocacao_id' in request.data:
        alocacao_horas = AlocacaoHoras.objects.get(pk=request.data['alocacao_id'])
    else:
        raise Exception('Alocação não selecionado')
    
    atividade_profissional = alocacao_horas.atividade_profissional
    
    tipo_alocacao = None
    if 'tipo_alocacao' in request.data:
        if request.data['tipo_alocacao']:
            tipo_alocacao = TipoAlocacao.objects.get(pk=request.data['tipo_alocacao']['id'])
        del request.data['tipo_alocacao']
    
    hora_inicio =  datetime.datetime.strptime(request.data['hora_inicio'], '%H:%M')
    hora_fim =  datetime.datetime.strptime(request.data['hora_fim'], '%H:%M')
    
    subtracao = hora_fim - hora_inicio
    if (subtracao.seconds * 1000) != request.data['horas_alocadas_milisegundos']:
        raise Exception("Milisegundos não confere")
    
    alocacao_horas.horas_alocadas_milisegundos = request.data['horas_alocadas_milisegundos']
    alocacao_horas.hora_inicio = request.data['hora_inicio']
    alocacao_horas.hora_fim= request.data['hora_fim']
    alocacao_horas.percentual_concluido= request.data['percentual_concluido']
    alocacao_horas.observacao= request.data['observacao'] if 'observacao' in request.data else None 
    alocacao_horas.data_informada = converter_string_para_data(request.data['data_informada'])
    alocacao_horas.data_alocacao = datetime.datetime.now()
    alocacao_horas.tipo_alocacao = tipo_alocacao
    alocacao_horas.save();
    
    alocacoes_horas = AlocacaoHoras.objects.filter(atividade_profissional =  atividade_profissional)
    
    total_milisegundos = 0
    maior_percentual_concluido = 0
    for i in alocacoes_horas:
        total_milisegundos += i.horas_alocadas_milisegundos
        if maior_percentual_concluido < i.percentual_concluido:
            maior_percentual_concluido = i.percentual_concluido
        
    atividade_profissional.horas_alocadas_milisegundos = total_milisegundos
    
    quantidade_horas_milisegundos = atividade_profissional.quantidade_horas * 60 * 60 * 1000
    percentual_calculado = (atividade_profissional.horas_alocadas_milisegundos * 100) / quantidade_horas_milisegundos 
    
    if percentual_calculado > 100:
        percentual_calculado = 100
    
    atividade_profissional.percentual_calculado = percentual_calculado
    atividade_profissional.percentual_concluido = maior_percentual_concluido
    atividade_profissional.save();
    
    #Calcular percentual atividade
    atividade = Atividade.objects.filter(atividadeprofissional = atividade_profissional)[0]
    atividades_profissionais = AtividadeProfissional.objects.filter(atividade = atividade)
    percentual_calculado = sum((a.percentual_calculado if a.percentual_calculado else 0) for a in atividades_profissionais) / len(atividades_profissionais);
    percentual_concluido = sum((a.percentual_concluido if a.percentual_concluido else 0) for a in atividades_profissionais) / len(atividades_profissionais);

    atividade.percentual_calculado = percentual_calculado
    atividade.percentual_concluido = percentual_concluido
    atividade.save();
    
    #calcular percentual fase_atividade
    fase_atividade = FaseAtividade.objects.filter(atividade = atividade)[0]
    atividades = Atividade.objects.filter(fase_atividade = fase_atividade)
    percentual_calculado = sum((a.percentual_calculado if a.percentual_calculado else 0) for a in atividades) / len(atividades);
    percentual_concluido = sum((a.percentual_concluido if a.percentual_concluido else 0) for a in atividades) / len(atividades);
    
    fase_atividade.percentual_calculado = percentual_calculado
    fase_atividade.percentual_concluido = percentual_concluido
    fase_atividade.save()
    
    demanda = Demanda.objects.filter(faseatividade = fase_atividade)[0]
    fase_atividades = FaseAtividade.objects.filter(demanda = demanda)
    percentual_calculado = sum((a.percentual_calculado if a.percentual_calculado else 0) for a in fase_atividades) / len(fase_atividades);
    percentual_concluido = sum((a.percentual_concluido if a.percentual_concluido else 0) for a in fase_atividades) / len(fase_atividades);
    
    demanda.percentual_calculado = percentual_calculado
    demanda.percentual_concluido = percentual_concluido
    demanda.save()
    
    return Response(AtividadeProfissionalSerializer(atividade_profissional).data)    