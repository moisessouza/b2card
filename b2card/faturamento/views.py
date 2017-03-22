from django.shortcuts import render
from rest_framework.views import APIView
from faturamento.models import Parcela, Medicao, ParcelaFase, PacoteItens,\
    LoteFaturamento, LoteDespesa, ItemDespesa
from faturamento.serializers import ParcelaSerializer, MedicaoSerializer, ParcelaFaseSerializer,\
    PacoteItensSerializer, LoteDespesaSerializer, ItemDespesaSerializer
from rest_framework.response import Response
from utils.utils import converter_string_para_float, converter_string_para_data, formatar_data,\
    formatar_para_valor_monetario, serializar_data
from demandas.models import Demanda, Orcamento, ItemFase, OrcamentoFase
from cadastros.models import ValorHora, TipoHora, Vigencia, PessoaFisica,\
    PessoaJuridica, Pessoa, TipoDespesa
from rest_framework.decorators import api_view
from demandas.serializers import OrcamentoFaseSerializer, OrcamentoSerializer,\
    ItemFaseSerializer
from cadastros.serializers import TipoHoraSerializer, ValorHoraSerializer, VigenciaSerializer
import datetime
from django.http.response import HttpResponse
from utils import docxgen
from utils.docxgen import realizar_replace_docx, gerar_arquivo_aprovacao
import importlib
import os
from django.db.models.aggregates import Sum
from django.db.models import F

# Create your views here.

def contas_receber_prevista(request):
    
    demandas = Demanda.objects.filter(parcela__status = 'PE').distinct()
    
    for demanda in demandas:
        parcelas = Parcela.objects.filter(demanda=demanda)
        demanda.parcelas=parcelas
    
    context = {
        'demandas': demandas
    }
    
    return render(request, 'contas_previstas/index.html', context);

class ParcelaList(APIView):
    
    def post(self, request, format=None):
        
        demanda = None
        if 'demanda_id' in request.data:
            demanda = Demanda.objects.get(pk=request.data['demanda_id'])
        else:
            raise Exception('Demanda nao informada');
        
        parcela_list = []
        if 'parcelas' in request.data:
            parcela_list = request.data['parcelas']
        
        parcela_resp = []
        for i in parcela_list:
            if 'remover' not in i or i['remover'] == False:
                
                valor_parcela = None
                if 'valor_parcela' in i:
                    valor_parcela = converter_string_para_float(i['valor_parcela'])
                    del i['valor_parcela']
                
                if 'demanda' in i:
                    del i['demanda']
               
                parcelafase_list = []
                if 'parcelafases' in i:
                    parcelafase_list = i['parcelafases']
                    del i['parcelafases']
                    
                if 'selecionado' in i:
                    del i['selecionado']
                
                pacote_itens = None
                selecionado = None
                if 'pacote_itens' in i and i['pacote_itens']:
                    pacote_itens = PacoteItens.objects.get(pk=i['pacote_itens']['id'])
                    selecionado = True
                    del i['pacote_itens']
                
                parcela = Parcela(**i)
                parcela.valor_parcela = valor_parcela
                parcela.data_previsto_parcela = converter_string_para_data(parcela.data_previsto_parcela)
                parcela.data_envio_aprovacao = converter_string_para_data(parcela.data_envio_aprovacao)
                parcela.data_aprovacao_faturamento = converter_string_para_data(parcela.data_aprovacao_faturamento)
                parcela.data_previsto_pagamento = converter_string_para_data(parcela.data_previsto_pagamento)
                parcela.data_faturamento = converter_string_para_data(parcela.data_faturamento)
                parcela.data_pagamento = converter_string_para_data(parcela.data_pagamento)
                parcela.pacote_itens = pacote_itens
                parcela.demanda = demanda
                parcela.save()
                
                parcelafase_resp = self.gravar_parcelafases(parcela, parcelafase_list)

                serializer = ParcelaSerializer(parcela).data
                serializer['data_previsto_parcela'] = formatar_data(parcela.data_previsto_parcela)
                serializer['data_envio_aprovacao'] = formatar_data(parcela.data_envio_aprovacao)
                serializer['data_aprovacao_faturamento'] = formatar_data(parcela.data_aprovacao_faturamento)
                serializer['data_previsto_pagamento'] = formatar_data(parcela.data_previsto_pagamento)
                serializer['data_faturamento'] = formatar_data(parcela.data_faturamento)
                serializer['data_pagamento'] = formatar_data(parcela.data_pagamento)
                serializer['selecionado'] = selecionado
                serializer['parcelafases'] = parcelafase_resp
                
                parcela_resp.append(serializer)
                
            elif 'id' in i:
                parcela = Parcela.objects.get(pk=i['id'])
                parcela.delete()
        
        context = {
            'parcelas': parcela_resp
        }
        
        return Response(context)
    
    def gravar_parcelafases(self, parcela, parcelafases):
    
        parcelafase_list = []
        if parcelafases:
            for i in parcelafases:
                if 'remover' not in i or i['remover'] == False:
                    
                    fase = None
                    if 'fase' in i:
                        fase = OrcamentoFase.objects.get(pk=i['fase']['id'])
                        del i['fase']
                    
                    if 'parcela' in i:
                        del i['parcela']
                        
                    medicoes = None
                    if 'medicoes' in i:
                        medicoes = i['medicoes']
                        del i['medicoes']
                    
                    parcela_fase = ParcelaFase(**i)
                    parcela_fase.valor = converter_string_para_float(parcela_fase.valor);
                    parcela_fase.parcela = parcela
                    parcela_fase.fase = fase
                    parcela_fase.save();
                    
                    data = ParcelaFaseSerializer(parcela_fase).data
                    
                    if medicoes:
                        medicao_list = self.gravar_medicoes(parcela_fase, medicoes)
                        data['medicoes'] = medicao_list
                        
                    parcelafase_list.append(data)
                
                elif 'id' in i:
                    parcela_fase = ParcelaFase.objects.get(pk=i['id'])
                    parcela_fase.delete()
                    
        return parcelafase_list        
    
    def gravar_medicoes(self, parcela_fase, medicoes):
        
        medicao_list = []
        if medicoes:
            for i in medicoes:
                if 'remover' not in i or i['remover'] == False:
                    
                    valor_hora = None
                    if 'valor_hora' in i:
                        valor_hora = ValorHora.objects.get(pk=i['valor_hora']['id'])
                        del i['valor_hora']
                    
                    medicao = Medicao(**i)
                    medicao.valor_hora = valor_hora
                    medicao.valor_total = converter_string_para_float(medicao.valor_total)
                    medicao.parcela_fase = parcela_fase
                    medicao.save()
                    medicao_list.append(MedicaoSerializer(medicao).data)
                    
                elif 'id' in i:
                    medicao = Medicao.objects.get(pk=i['id'])
                    medicao.delete()
         
        return medicao_list
    
    
@api_view(['GET'])
def buscar_parcela_por_demanda_id(request, demanda_id, format=None):

    parcelas = Parcela.objects.filter(demanda__id=demanda_id)
    parcelas_list = []

    for i in parcelas:
        
        parcela_data = ParcelaSerializer(i).data
        parcela_data['parcelafases'] = []
        parcela_data['data_previsto_parcela'] = formatar_data(i.data_previsto_parcela)
        parcela_data['data_envio_aprovacao'] = formatar_data(i.data_envio_aprovacao)
        parcela_data['data_aprovacao_faturamento'] = formatar_data(i.data_aprovacao_faturamento)
        parcela_data['data_previsto_pagamento'] = formatar_data(i.data_previsto_pagamento)
        parcela_data['data_faturamento'] = formatar_data(i.data_faturamento)
        parcela_data['data_pagamento'] = formatar_data(i.data_pagamento)
        parcelas_list.append(parcela_data)
        
        parcelafases_list = ParcelaFase.objects.filter(parcela = i)
        for pf in parcelafases_list:
            pf_data = ParcelaFaseSerializer(pf).data
            medicoes_list = Medicao.objects.filter(parcela_fase = pf)
            pf_data['medicoes'] = MedicaoSerializer(medicoes_list, many=True).data
            
            parcela_data['parcelafases'].append(pf_data);
        
    
    return Response(parcelas_list);

@api_view(['GET'])
def buscar_tipo_hora_por_fases(request, demanda_id, format=None):
    
    fase_list = OrcamentoFase.objects.filter(orcamento__demanda__id=demanda_id)
    
    faseserializer_list = []
    
    for i in fase_list:
        serializer = OrcamentoFaseSerializer(i).data
        faseserializer_list.append(serializer)
        valor_horas = ValorHora.objects.filter(itemfase__orcamento_fase = i).distinct()
        
        valor_hora_list = []
        for i in valor_horas:
            vigencia = Vigencia.objects.filter(valor_hora=i, data_inicio__lte = datetime.date.today(), data_fim__gte = datetime.date.today())
            if vigencia:
                valor_hora_data = ValorHoraSerializer(i).data    
                valor_hora_data['vigencia'] = VigenciaSerializer(vigencia[0]).data
                valor_hora_list.append(valor_hora_data)
        
        serializer['valorhora'] = valor_hora_list
        
    
    return Response(faseserializer_list)

@api_view(['POST'])
def search_contas_receber(request, format=None):
    
    data = request.data;
    
    argumentos = {}
    
    if 'demanda_id' in data and data['demanda_id']:
        argumentos['demanda__id'] = data['demanda_id']
    
    if 'mes' in data and len(data['mes']) > 0:
        date = data['mes']
        mes = date[0:date.index('/')]
        ano = date[date.index('/') + 1 : len(date)]
        argumentos['data_previsto_parcela__month'] = mes
        argumentos['data_previsto_parcela__year'] = ano
    
    if 'cliente_id' in data:
        argumentos['demanda__cliente__id'] = data['cliente_id']
    
    if 'status' in data:
        argumentos['status'] = data['status']
        
    if not request.user.is_superuser:
        pessoa_fisica = PessoaFisica.objects.filter(prestador__usuario__id=request.user.id)[0]
        unidade_administrativas = pessoa_fisica.unidade_administrativas.all()
        argumentos['demanda__unidade_administrativa__in']=unidade_administrativas
    
    parcelas = Parcela.objects.filter(**argumentos);
    
    parcela_list = []
    for i in parcelas:
        parcela = ParcelaSerializer(i).data
        parcelafases = ParcelaFase.objects.filter(parcela = i)
        parcelafases = ParcelaFaseSerializer(parcelafases, many=True).data
        parcela['parcelafases'] = parcelafases
        parcela_list.append(parcela) 
    
    return Response(parcela_list)

@api_view(['GET'])
def buscar_orcamento_demanda_id(request, demanda_id, format=None):
    
    orcamento = Orcamento.objects.filter(demanda__id = demanda_id);
    data = OrcamentoSerializer(orcamento[0]).data
    
    fases = OrcamentoFase.objects.filter(orcamento = orcamento);
    fases = OrcamentoFaseSerializer(fases, many=True).data
    
    for i in fases:
        itensfase = ItemFase.objects.filter(orcamento_fase__id = i['id'])
        itensfase = ItemFaseSerializer(itensfase, many=True).data
        i['itensfase'] = itensfase
    
    data['fases'] = fases
    
    return Response(data);

@api_view(['GET'])
def buscar_pacote_itens_cliente(request, cliente_id, format=None):

    try:
        pacote_itens = PacoteItens.objects.filter(cliente__id=cliente_id, status='P').order_by('-pk')[0]
    except IndexError:
        pacote_itens = PacoteItens()
        pacote_itens.cliente = PessoaJuridica.objects.get(pk=cliente_id)
        pacote_itens.status = 'P'
        pacote_itens.data_criacao = datetime.date.today()
        pacote_itens.save()
    except:
        raise
    
    #buscar por pacotes recusados
    try:
        recusados = PacoteItens.objects.filter(cliente__id = cliente_id, status='R')
        if recusados:
            for r in recusados:
                parcelas_recusadas = Parcela.objects.filter(pacote_itens = r)
                if parcelas_recusadas:
                    for pr in parcelas_recusadas:
                        pr.pacote_itens = pacote_itens
                        pr.save()
                r.status = 'D'
    except:
        raise
    
    lista_itens = Parcela.objects.filter(pacote_itens = pacote_itens)
    pacote_itens = PacoteItensSerializer(pacote_itens).data
    
    if lista_itens:
        lista_itens = ParcelaSerializer(lista_itens, many=True).data
        for i in lista_itens:
            
            i['valor_parcela'] = formatar_para_valor_monetario(i['valor_parcela'])
            i['data_previsto_parcela'] = serializar_data(i['data_previsto_parcela'])
            
            parcela_fases = ParcelaFase.objects.filter(parcela__id = i['id'])
            parcela_fases = ParcelaFaseSerializer(parcela_fases, many=True).data
            
            if parcela_fases:
                for p in parcela_fases:
                    
                    medicoes = Medicao.objects.filter(parcela_fase__id = p['id'])
                    medicoes = MedicaoSerializer(medicoes, many=True).data
                    if medicoes:
                        for m in medicoes:
                            m['valor_total'] = formatar_para_valor_monetario(m['valor_total'])
                    p['medicoes'] = medicoes
            i['parcelafases'] = parcela_fases
    
            pacote_itens['lista_itens'] = lista_itens
    
    return Response(pacote_itens)

@api_view(['POST'])
def criar_pacote_itens(request, format=None):
    
    valor_total = request.data['valor_total']
    total_horas = request.data['total_horas']
    cliente_id = request.data['cliente_id']
    
    if 'id' in request.data and request.data['id']:
        pacote_itens = PacoteItens.objects.get(pk=request.data['id'])
        parcelas = Parcela.objects.filter(pacote_itens = pacote_itens)
        
        if parcelas:
            for i in parcelas:
                i.pacote_itens = None
                i.status = 'PE'
                i.save()
        
    else:
        pacote_itens = PacoteItens()
        pessoa_juridica = PessoaJuridica.objects.get(pk = cliente_id)
        pacote_itens.cliente = pessoa_juridica
        pacote_itens.data_criacao = datetime.date.today()
        pacote_itens.status = 'P'
        
    pacote_itens.valor_total = converter_string_para_float(valor_total)
    pacote_itens.total_horas = total_horas
    pacote_itens.data_criacao = datetime.date.today()
    pacote_itens.save()

    lista_itens = request.data['lista_itens']
    
    if lista_itens:
        for i in lista_itens:
            if 'id' in i and i['id']:
                parcela = Parcela.objects.get(pk=i['id'])
                parcela.status = i['status']
                parcela.pacote_itens = pacote_itens
                parcela.save()
                
    return Response(PacoteItensSerializer(pacote_itens).data)

@api_view(['POST'])
def enviar_para_aprovacao(request):
    
    pacote_itens = PacoteItens.objects.get(pk=request.data['id'])
    parcelas = Parcela.objects.filter(pacote_itens = pacote_itens)
    
    if parcelas:
        for i in parcelas:
            i.status = 'PA'
            i.save()
    
    return Response(PacoteItensSerializer(pacote_itens).data)

@api_view(['POST'])
def enviar_para_faturamento(request):
    
    pacote_itens = PacoteItens.objects.get(pk = request.data['id'])
    pacote_itens.status = 'E'
    pacote_itens.save()
    
    parcelas = Parcela.objects.filter(pacote_itens = pacote_itens)
    if parcelas:
        lote_faturamento = LoteFaturamento()
        lote_faturamento.data_criacao = datetime.date.today()
        lote_faturamento.save()
        
        for p in parcelas:
            p.lote_faturamento = lote_faturamento
            p.status ='PF'
            p.save()
            
    return Response(PacoteItensSerializer(pacote_itens).data)

PASTA_ARQUIVOS = importlib.import_module(os.environ['DJANGO_SETTINGS_MODULE']).PASTA_ARQUIVOS

def buscar_arquivo_template(demanda_id):
    
    pessoa_juridica = PessoaJuridica.objects.filter(demanda__id=demanda_id).order_by('-id')[0]
    
    if pessoa_juridica.arquivo:
        arquivo_template = pessoa_juridica.arquivo.path_arquivo
    else: 
        arquivo_template = PASTA_ARQUIVOS + 'template.docx'
        
    return arquivo_template

def gerar_arquivo_faturamento(request, demanda_id):
    
    arquivo_template = buscar_arquivo_template(demanda_id)
    
    arquivo_gerado = realizar_replace_docx(demanda_id, arquivo_template, 'T')

    response = HttpResponse(arquivo_gerado.getvalue(), content_type='application/force-download')
    response['Content-Disposition'] = 'attachment; filename="proposta_tecnica.docx"'
    return response

def gerar_arquivo_faturamento_comercial(request, demanda_id):
    
    arquivo_template = buscar_arquivo_template(demanda_id)
    
    arquivo_gerado = realizar_replace_docx(demanda_id, arquivo_template, 'C')

    response = HttpResponse(arquivo_gerado.getvalue(), content_type='application/force-download')
    response['Content-Disposition'] = 'attachment; filename="proposta_comercial.docx"'
    return response

def gerar_arquivo_aprovacao(request, pacote_itens_id):
    
    pacote_itens = PacoteItens.objects.filter(pk=pacote_itens_id).values('parcela__demanda__id', 'parcela__demanda__nome_demanda', 'parcela__demanda__codigo_demanda', 
                           'parcela__parcelafase__fase__fase__descricao', 'parcela__parcelafase__fase__fase__id',
                           'parcela__parcelafase__medicao__valor_hora__id', 'parcela__parcelafase__medicao__valor_hora__descricao').distinct()
    
    for v in pacote_itens:
        
        valor_hora_id = v['parcela__parcelafase__medicao__valor_hora__id']
        demanda_id = v['parcela__demanda__id']
        #parcelafase_id = v['parcela__parcelafase__id']
        fase__id = v['parcela__parcelafase__fase__fase__id']
        
        horas_contratadas = ParcelaFase.objects.filter(parcela__demanda__id = demanda_id,
                                medicao__valor_hora__id=valor_hora_id, fase__fase__id=fase__id).distinct().aggregate(horas_contratadas= Sum('medicao__quantidade_horas'))['horas_contratadas']
                                
        horas_ja_faturadas = Medicao.objects.filter(parcela_fase__parcela__status__in = ['FA', 'PG'], parcela_fase__parcela__demanda__id = demanda_id, valor_hora__id=valor_hora_id, parcela_fase__fase__fase__id = fase__id).distinct().aggregate(quantidade_horas = Sum('quantidade_horas'))['quantidade_horas']
                                
        #saldo_a_faturar = ParcelaFase.objects.filter(parcela__status__in = ['PA', 'FA', 'PG'], 
        #                       parcela__demanda__id = demanda_id,parcela__parcelafase__medicao__valor_hora__id=valor_hora_id, parcela__parcelafase__fase__fase__id=fase__id).aggregate(saldo_a_faturar= Sum('parcela__parcelafase__medicao__quantidade_horas'))['saldo_a_faturar']
        
        saldo_a_faturar = round(horas_contratadas - (horas_ja_faturadas if horas_ja_faturadas else 0), 2)
        
        valor_por_hora = ParcelaFase.objects.filter(parcela__status__in = ['PA'],
                                parcela__demanda__id = demanda_id,parcela__parcelafase__medicao__valor_hora__id=valor_hora_id).annotate(valor_por_hora=F('parcela__parcelafase__medicao__valor_total')/F('parcela__parcelafase__medicao__quantidade_horas'))[0].valor_por_hora
                                
        horas_a_faturar = Medicao.objects.filter(parcela_fase__parcela__status__in = ['PA'], parcela_fase__parcela__demanda__id = demanda_id, valor_hora__id=valor_hora_id, parcela_fase__fase__fase__id = fase__id).distinct().aggregate(quantidade_horas = Sum('quantidade_horas'))['quantidade_horas']                       
        
        valor_a_faturar = ParcelaFase.objects.filter(parcela__status__in = ['PA'],
                                parcela__demanda__id = demanda_id,parcela__parcelafase__medicao__valor_hora__id=valor_hora_id).distinct().aggregate(valor_total = Sum('parcela__parcelafase__medicao__valor_total'))['valor_total']
    
        v['horas_contratadas'] = horas_contratadas
        v['horas_ja_faturadas'] = horas_ja_faturadas
        v['saldo_a_faturar'] = saldo_a_faturar
        v['valor_por_hora'] = valor_por_hora
        v['horas_a_faturar'] = horas_a_faturar
        v['valor_a_faturar'] = valor_a_faturar
    
    arquivo_template = PASTA_ARQUIVOS + 'template_aprovacao.docx'
    
    arquivo_gerado = docxgen.gerar_arquivo_aprovacao(arquivo_template, pacote_itens)
    
    response = HttpResponse(arquivo_gerado.getvalue(), content_type='application/force-download')
    response['Content-Disposition'] = 'attachment; filename="tabela_aprovacao.docx"'
    return response

@api_view(['POST'])
def gerar_lote_despesas(request, format=None):
     
    demanda = None
    if 'demanda' in request.data:
        if 'id' in request.data['demanda'] and request.data['demanda']['id']:
            demanda = Demanda.objects.get(pk=request.data['demanda']['id'])
        del request.data['demanda']
        
    if 'pessoa' in request.data:
        del request.data['pessoa']

    pessoa = Pessoa.objects.filter(pessoafisica__prestador__usuario__id = request.user.id)[0]
        
    item_despesas = []
    if 'item_despesas' in request.data:
        item_despesas = request.data['item_despesas']
        del request.data['item_despesas']
        
    lote_despesa = LoteDespesa(**request.data)
    lote_despesa.demanda = demanda
    lote_despesa.pessoa = pessoa
    lote_despesa.status = 'PE'
    lote_despesa.data = datetime.datetime.now().date()
    lote_despesa.valor_total = converter_string_para_float(lote_despesa.valor_total)
    lote_despesa.save()
    
    item_despesa_list = []
    for i in item_despesas:
        if 'remover' not in i or i['remover'] is False:
            
            tipo_despesa = None
            if 'tipo_despesa' in i:
                if 'id' in i['tipo_despesa'] and i['tipo_despesa']['id']:
                    tipo_despesa = TipoDespesa.objects.get(pk=i['tipo_despesa']['id'])
                del i['tipo_despesa']
            
            item_despesa = ItemDespesa(**i)
            item_despesa.lote_despesa = lote_despesa
            item_despesa.tipo_despesa = tipo_despesa
            item_despesa.data = converter_string_para_data(item_despesa.data)
            item_despesa.valor = converter_string_para_float(item_despesa.valor)
            item_despesa.save()
            
            item_despesa_list.append(item_despesa)
            
        elif 'id' in i:
            item_despesa = ItemDespesa.objects.get(pk=i['id'])
            item_despesa.delete()
    
    data = LoteDespesaSerializer(lote_despesa).data
    
    item_despesa_list = ItemDespesaSerializer(item_despesa_list, many=True).data
    
    for i in item_despesa_list:
        i['valor'] = formatar_para_valor_monetario(i['valor'])
        i['data'] = serializar_data(i['data'])
    
    data['item_despesas'] =  item_despesa_list
    
    return Response(data)

@api_view(['GET'])
def buscar_lote_despesas_abertos(request, demanda_id, format=None):
    
    lote_despesas = LoteDespesa.objects.filter(pessoa__pessoafisica__prestador__usuario__id = request.user.id, status='PE', demanda__id = demanda_id)
    
    if lote_despesas:
        lote_despesa_list = LoteDespesaSerializer(lote_despesas, many=True).data;
        for l in lote_despesa_list:
            
            l['valor_total'] = formatar_para_valor_monetario(l['valor_total'])
            
            item_despesa = ItemDespesa.objects.filter(lote_despesa__id = l['id'])
            
            item_despesa_list = ItemDespesaSerializer(item_despesa, many=True).data
            for i in item_despesa_list:
                i['valor'] = formatar_para_valor_monetario(i['valor'])
                i['data'] = serializar_data(i['data'])
                
            l['item_despesas'] = item_despesa_list
        
        return Response(lote_despesa_list)
    
    return Response([])


def relatorio_despesas(request, lote_despesa_id):
    
    lote_despesa = LoteDespesa.objects.get(pk=lote_despesa_id)
    item_despesas = ItemDespesa.objects.filter(lote_despesa = lote_despesa)
    
    lote_despesa.valor_total = formatar_para_valor_monetario(lote_despesa.valor_total)
    #lote_despesa.data = serializar_data(lote_despesa.data)
    
    for i in item_despesas:
        
        i.valor = formatar_para_valor_monetario(i.valor)
       # i.data = serializar_data(i.data)
    
    context = {
        'lote_despesa':lote_despesa,
        'item_despesas': item_despesas
    }
    
    return render(request, 'relatorio/relatorio_despesas.html', context)
    