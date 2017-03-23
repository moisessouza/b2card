# -*- coding: utf-8 -*-
from django.shortcuts import render
from rest_framework.decorators import api_view
from demandas.models import Atividade, Demanda, FaseAtividade,\
    AtividadeProfissional, AlocacaoHoras
from demandas.serializers import DemandaSerializer, AtividadeSerializer,\
    FaseAtividadeSerializer, AtividadeProfissionalSerializer,\
    AlocacaoHorasSerializer, DemandaInicialSerializer,\
    FaseAtividadeInicialSerializer, AtividadeProfissionalInicialSerializer
from rest_framework.response import Response
from cadastros.models import PessoaJuridica, TipoAlocacao, PessoaFisica,\
    CustoPrestador
from cadastros.serializers_pessoa import PessoaJuridicaSerializer,\
    PessoaJuridicaComPessoaSerializer
from utils.utils import formatar_data, converter_string_para_data,\
    converter_data_url
import datetime
from django.db.models import Q
from django.db.models.aggregates import Sum

# Create your views here.
def index (request):
    return render(request, 'first_page.html')

@api_view(['POST'])
def buscar_atividades_usuario(request, format=None):

    clientes  = PessoaJuridica.objects.filter(demanda__faseatividade__atividade__atividadeprofissional__pessoa_fisica__prestador__usuario__id=request.user.id).distinct()
    cliente_list = [];

    list_status = []
    if request.data:
        for k in request.data:
            if request.data[k]:
                list_status.append(k)

    for c in clientes:
        
        if list_status:
            demandas = Demanda.objects.filter(status_demanda__in=list_status).filter(Q(tipo_demanda='E') | Q(tipo_demanda=None), cliente = c, faseatividade__atividade__atividadeprofissional__pessoa_fisica__prestador__usuario__id=request.user.id).distinct();
        else:
            demandas = Demanda.objects.filter(Q(tipo_demanda='E') | Q(tipo_demanda=None), cliente = c, faseatividade__atividade__atividadeprofissional__pessoa_fisica__prestador__usuario__id=request.user.id).distinct();
        demanda_list = []

        for i in demandas:
            demanda_dict = DemandaInicialSerializer(i).data
            demanda_list.append(demanda_dict)
        
        if demanda_list:
            cliente_dict = PessoaJuridicaComPessoaSerializer(c).data    
            cliente_dict['demandas'] = demanda_list
            cliente_list.append(cliente_dict)
        
    return Response(cliente_list)

@api_view(['POST'])
def buscar_atividades_internas(request, format=None):
    
    clientes = PessoaJuridica.objects.all()
    cliente_list = [];
    
    list_status = []
    if request.data:
        for k in request.data:
            if request.data[k]:
                list_status.append(k)
    
    for c in clientes:
        
        if list_status:
            demandas = Demanda.objects.filter(status_demanda__in=list_status).filter(tipo_demanda='I', cliente = c).distinct();
        else:
            demandas = Demanda.objects.filter(tipo_demanda='I', cliente = c).distinct();
    
        demanda_list = []
        
        for i in demandas:
            demanda_dict = DemandaInicialSerializer(i).data
            demanda_list.append(demanda_dict)
        
        if demanda_list:
            cliente_dict = PessoaJuridicaComPessoaSerializer(c).data    
            cliente_dict['demandas'] = demanda_list
            cliente_list.append(cliente_dict)
    
    return Response(cliente_list)

@api_view(['GET'])
def buscar_alocacao_dia(request, data_informada, format=None):
    
    data = converter_data_url(data_informada)
    alocacao_horas = (AlocacaoHoras.objects.filter(data_informada = data, atividade_profissional__pessoa_fisica__prestador__usuario__id=request.user.id)
        .values('hora_inicio', 'hora_fim', 'horas_alocadas_milisegundos', 'atividade_profissional__atividade__descricao'))
    
    total_horas = (AlocacaoHoras.objects.filter(data_informada = data, atividade_profissional__pessoa_fisica__prestador__usuario__id=request.user.id)
        .aggregate(total_horas = Sum('horas_alocadas_milisegundos')))
    
    context = {
        'alocacao_horas': alocacao_horas,
        'total':total_horas
    }
    
    return Response(context)

@api_view(['GET'])
def buscar_atividades_demanda(request, demanda_id, format=None):

    fase_atividades = FaseAtividade.objects.filter(demanda__id=demanda_id, atividade__atividadeprofissional__pessoa_fisica__prestador__usuario__id=request.user.id).distinct();
    fase_atividade_list = []
    
    for f in fase_atividades:

        fase_atividade_dict = FaseAtividadeInicialSerializer(f).data
        fase_atividade_list.append(fase_atividade_dict)
        
        atividades = Atividade.objects.filter(fase_atividade=f,atividadeprofissional__pessoa_fisica__prestador__usuario__id=request.user.id).distinct()
        atividade_list = [];
        
        for a in atividades:
            
            atividade_dict = AtividadeSerializer(a).data
            atividade_dict['data_inicio'] = formatar_data(a.data_inicio)
            atividade_dict['data_fim'] = formatar_data(a.data_fim)
            atividade_list.append(atividade_dict)
            atividade_profissional =  AtividadeProfissional.objects.filter(atividade = a, pessoa_fisica__prestador__usuario__id=request.user.id)[:1]
            
            atividade_profissional_dict = AtividadeProfissionalInicialSerializer(atividade_profissional[0]).data
            atividade_dict['atividade_profissional'] = atividade_profissional_dict
            
        fase_atividade_dict['atividades']=atividade_list
            
    return Response(fase_atividade_list)  

@api_view(['GET'])
def buscar_atividades_demanda_interna(request, demanda_id, format=None):
    
    fase_atividades = FaseAtividade.objects.filter(demanda__id=demanda_id)
    fase_atividade_list = []
    
    for f in fase_atividades:
        fase_atividade_dict = FaseAtividadeInicialSerializer(f).data
        fase_atividade_list.append(fase_atividade_dict)
        
        atividades = Atividade.objects.filter(fase_atividade=f).distinct()
        atividade_list = [];
        
        for a in atividades:
            
            atividade_dict = AtividadeSerializer(a).data
            atividade_dict['data_inicio'] = formatar_data(a.data_inicio)
            atividade_dict['data_fim'] = formatar_data(a.data_fim)
            atividade_list.append(atividade_dict)
            
            atividade_profissional =  AtividadeProfissional.objects.filter(atividade = a, pessoa_fisica__prestador__usuario__id=request.user.id)[:1]
            if atividade_profissional:
                atividade_profissional_dict = AtividadeProfissionalInicialSerializer(atividade_profissional[0]).data
                atividade_dict['atividade_profissional'] = atividade_profissional_dict
            
        fase_atividade_dict['atividades']=atividade_list
    
    return Response(fase_atividade_list)  

@api_view(['POST'])
def alocar_horas_internas(request, format=None):
    
    atividade_profissional = None
    if 'atividade_profissional' in request.data:
        atividade_profissional = AtividadeProfissional.objects.get(pk=request.data['atividade_profissional']['id'])
        del request.data['atividade_profissional']
        
    if 'atividade' in request.data:
        if atividade_profissional is None:
            atividade = Atividade.objects.get(pk=request.data['atividade']['id'])
            atividade_profissional = AtividadeProfissional()
            atividade_profissional.atividade = atividade
            pessoa_fisica = PessoaFisica.objects.filter(prestador__usuario__id=request.user.id)[0]
            atividade_profissional.pessoa_fisica = pessoa_fisica
            atividade_profissional.quantidade_horas = 0
            atividade_profissional.percentual_calculado = 0
            atividade_profissional.percentual_concluido = 0
            atividade_profissional.save()
        del request.data['atividade']
    
    alocacao_horas = AlocacaoHoras(**request.data)
    alocacao_horas.atividade_profissional = atividade_profissional
    alocacao_horas.data_informada = converter_string_para_data(request.data['data_informada'])
    alocacao_horas.data_alocacao = datetime.datetime.now()
    
    if 'observacao' in request.data and request.data['observacao']:
        alocacao_horas.observacao = request.data['observacao']
    else:
        alocacao_horas.observacao = None
    
    alocacao_horas.percentual_concluido = 0
    alocacao_horas.save();
    
    horas_alocadas_milisegundos = request.data['horas_alocadas_milisegundos']
    
    if (atividade_profissional.horas_alocadas_milisegundos):
        atividade_profissional.horas_alocadas_milisegundos += horas_alocadas_milisegundos
    else:
        atividade_profissional.horas_alocadas_milisegundos = horas_alocadas_milisegundos
        
    atividade_profissional.save();

    return Response(AtividadeProfissionalSerializer(atividade_profissional).data)
        
@api_view(['POST'])
def alocar_horas(request, format=None):
    
    atividade_profissional = None
    if 'atividade_profissional' in request.data:
        atividade_profissional = AtividadeProfissional.objects.get(pk=request.data['atividade_profissional']['id'])
        del request.data['atividade_profissional']
    
    
    
    tipo_alocacao = None
    if 'tipo_alocacao' in request.data:
        tipo_alocacao = TipoAlocacao.objects.get(pk=request.data['tipo_alocacao']['id'])
        del request.data['tipo_alocacao']
    
    hora_inicio =  datetime.datetime.strptime(request.data['hora_inicio'], '%H:%M')
    hora_fim =  datetime.datetime.strptime(request.data['hora_fim'], '%H:%M')
    
    subtracao = hora_fim - hora_inicio
    if (subtracao.seconds * 1000) != request.data['horas_alocadas_milisegundos']:
        raise Exception("Milisegundos não confere")
    
    alocacao_horas = AlocacaoHoras(**request.data)
    alocacao_horas.atividade_profissional = atividade_profissional
    alocacao_horas.data_informada = converter_string_para_data(request.data['data_informada'])
    alocacao_horas.data_alocacao = datetime.datetime.now()
    alocacao_horas.tipo_alocacao = tipo_alocacao
    alocacao_horas.save();
    
    horas_alocadas_milisegundos = request.data['horas_alocadas_milisegundos']
    percentual_concluido = request.data['percentual_concluido']    
    
    if (atividade_profissional.horas_alocadas_milisegundos):
        atividade_profissional.horas_alocadas_milisegundos += horas_alocadas_milisegundos
    else:
        atividade_profissional.horas_alocadas_milisegundos = horas_alocadas_milisegundos
    
    quantidade_horas_milisegundos = atividade_profissional.quantidade_horas * 60 * 60 * 1000
    percentual_calculado = (atividade_profissional.horas_alocadas_milisegundos * 100) / quantidade_horas_milisegundos 
    
    if percentual_calculado > 100:
        percentual_calculado = 100
    
    atividade_profissional.percentual_calculado = percentual_calculado
    atividade_profissional.percentual_concluido = percentual_concluido
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

@api_view(['GET'])
def buscar_ultima_alocacao(request, atividade_profissional_id, format=None):
    
    alocacao_horas = AlocacaoHoras.objects.filter(atividade_profissional__id = atividade_profissional_id).order_by('-id')[:1]
    if alocacao_horas:
        return Response(AlocacaoHorasSerializer(alocacao_horas[0]).data)
    else:
        return Response({})
    
@api_view(['GET'])
def buscar_atividade_profissional_por_atividade(request, atividade_id, format=None):
    
    atividade_profissional =  AtividadeProfissional.objects.filter(atividade__id = atividade_id, pessoa_fisica__prestador__usuario__id=request.user.id)[:1]
    atividade_profissional_dict = AtividadeProfissionalSerializer(atividade_profissional[0]).data
    
    return Response(atividade_profissional_dict)

@api_view(['GET'])
def validar_data_hora(request, data_informada, hora_inicio, hora_fim, format=None):
    
    data = converter_data_url(data_informada)
    
    custo_prestador = CustoPrestador.objects.filter(pessoa_fisica__prestador__usuario__id=request.user.id, data_inicio__lte=data).filter(Q(data_fim__isnull = True) | Q(data_fim__gte = data))
    
    result = {}
    
    if len(custo_prestador) > 0:
        result['custo_prestador'] = True
    else:
        result['custo_prestador'] = False
    
    
    alocacoes = AlocacaoHoras.objects.filter(atividade_profissional__pessoa_fisica__prestador__usuario__id=request.user.id, data_informada = data)
    
    hora_inicio =  datetime.datetime.strptime(hora_inicio, '%H:%M')
    hora_fim =  datetime.datetime.strptime(hora_fim, '%H:%M')
    
    for i in alocacoes:
        
        hora_inicio_aloc =  datetime.datetime.strptime(i.hora_inicio, '%H:%M')
        hora_fim_aloc =  datetime.datetime.strptime(i.hora_fim, '%H:%M')
        
        if hora_inicio > hora_inicio_aloc and hora_inicio < hora_fim_aloc:
            result['possui_alocacao'] = True
            break
        elif hora_fim > hora_inicio_aloc and hora_fim < hora_fim_aloc:
            result['possui_alocacao']  = True
            break
        elif hora_inicio <= hora_inicio_aloc and hora_fim >= hora_fim_aloc:
            result['possui_alocacao']  = True
            break
            
            
    return Response(result)