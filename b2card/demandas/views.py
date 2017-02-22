# -*- coding: utf-8 -*-
from django.db.models.aggregates import Sum
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

from rest_framework.views import APIView
from django.core.paginator import Paginator
from django.db.models import Q

from cadastros.models import CentroCusto, ValorHora, UnidadeAdministrativa, \
    PessoaFisica, PessoaJuridica, NaturezaDemanda
from demandas.models import Demanda, Proposta, Observacao, Ocorrencia, \
    Orcamento, ItemFase, Fase, Atividade, OrcamentoFase, \
    OrcamentoAtividade, PerfilAtividade, AtividadeProfissional, FaseAtividade,\
    AlocacaoHoras, Despesa
from demandas.serializers import DemandaSerializer, PropostaSerializer, \
    ObservacaoSerializer, OcorrenciaSerializer, OrcamentoSerializer, \
    ItemFaseSerializer, AtividadeSerializer, \
    OrcamentoFaseSerializer, OrcamentoAtividadeSerializer, \
    AtividadeProfissionalSerializer, FaseAtividadeSerializer,\
    DemandaInicialSerializer, DespesaSerializer
from faturamento.models import Parcela, Medicao, ParcelaFase
from faturamento.serializers import ParcelaSerializer, MedicaoSerializer, ParcelaFaseSerializer
from utils.utils import converter_string_para_data, formatar_data, converter_string_para_float,\
    serializar_data
from django.db.models.functions.base import Coalesce


# Create your views here.
def index(request):
    
    demandas = Demanda.objects.all()
    
    context = {
        'demandas': demandas
    }
    return render(request, 'demandas/index.html', context)
    
def novo(request):
    return render(request, 'demandas/demanda.html')

def editar(request, demanda_id):
    
    demanda = Demanda.objects.get(pk=demanda_id)
    
    context = {
        'demanda': demanda
    }
    
    return render(request, 'demandas/demanda.html', context)

def serializarDemanda(demanda_id):
    demanda = Demanda.objects.get(pk=demanda_id)
    return serializarDemandaObject(demanda)

def serializarDemandaObject(demanda):
       
    propostas = Proposta.objects.filter(demanda__id=demanda.id)
    observacoes = Observacao.objects.filter(demanda__id=demanda.id)
    ocorrencias = Ocorrencia.objects.filter(demanda__id=demanda.id)
    orcamentos = Orcamento.objects.filter(demanda__id=demanda.id)
    #fase_atividades = FaseAtividade.objects.filter(demanda__id=demanda.id)
    parcelas = Parcela.objects.filter(demanda__id=demanda.id)
    
    data = DemandaSerializer(demanda).data
    
    data['data_criacao'] = formatar_data(demanda.data_criacao)
    
    propostas_list = PropostaSerializer(propostas, many=True).data
    for i in propostas_list:
        if 'data_recimento_solicitacao' in i:
            i['data_recimento_solicitacao'] = serializar_data(i['data_recimento_solicitacao'])
        if 'data_limite_entrega' in i:
            i['data_limite_entrega'] = serializar_data(i['data_limite_entrega'])
        if 'data_real_entrega' in i:
            i['data_real_entrega'] = serializar_data(i['data_real_entrega'])
        if 'data_aprovacao' in i:
            i['data_aprovacao'] = serializar_data(i['data_aprovacao'])
    
    observacoes_list = ObservacaoSerializer(observacoes, many=True).data
    for i in observacoes_list:
        if 'data_observacao' in i:
            i['data_observacao'] = serializar_data(i['data_observacao'])
        
    ocorrencias_list = OcorrenciaSerializer(ocorrencias, many=True).data
    for i in ocorrencias_list:
        if 'data_solicitacao' in i:
            i['data_solicitacao'] = serializar_data(i['data_solicitacao'])
        if 'data_prevista_conclusao' in i:
            i['data_prevista_conclusao'] = serializar_data(i['data_prevista_conclusao'])
        
    orcamento_dict = serializar_orcamento(orcamentos)
    
    #fase_atividade_list = serializar_fase_atividade(fase_atividades)
        
    parcelas_list = ParcelaSerializer(parcelas, many=True).data
    for i in parcelas_list:
        
        i['data_previsto_parcela'] = serializar_data(i['data_previsto_parcela'])
        
        parcelafase_list = ParcelaFase.objects.filter(parcela = i['id'])
        parcelafaseserializer_list = ParcelaFaseSerializer(parcelafase_list, many=True).data
        
        for pf in parcelafaseserializer_list:
            medicoes = Medicao.objects.filter(parcela_fase__id = pf['id'])
            medicao_list = MedicaoSerializer(medicoes, many=True).data
            pf['medicoes'] = medicao_list
        i['parcelafases'] = parcelafaseserializer_list

    data['propostas'] = propostas_list
    data['observacoes'] = observacoes_list
    data['ocorrencias'] = ocorrencias_list
    data['orcamento'] = orcamento_dict
    #data['fase_atividades'] = fase_atividade_list
    data['parcelas'] = parcelas_list
   
    return data

def serializar_orcamento(orcamentos):
        
    orcamento_dict = {}
    if  orcamentos:
        orcamento = orcamentos[0]
        orcamento_dict = OrcamentoSerializer(orcamento).data
        orcamento_fases = OrcamentoFase.objects.filter(orcamento = orcamento)
        
        fases_list = OrcamentoFaseSerializer(orcamento_fases, many=True).data
        for i in fases_list:
            itens_fase = ItemFase.objects.filter(orcamento_fase__id = i['id'])
            intes_fase_list = ItemFaseSerializer(itens_fase, many=True).data
            i['itensfase'] = intes_fase_list
            
        orcamento_dict['orcamento_fases'] = fases_list
        
        orcamento_atividades = OrcamentoAtividade.objects.filter(orcamento = orcamento)
        orcamento_atividades_list = OrcamentoAtividadeSerializer(orcamento_atividades, many=True).data
        
        if orcamento_atividades_list:
            for o in orcamento_atividades_list:
                perfil_atividades = PerfilAtividade.objects.filter(orcamento_atividade__id = o['id'])
                dict = {}
                for p in perfil_atividades:
                    dict[p.perfil.id] = { 'horas': p.horas }
                o['colunas'] = dict

        orcamento_dict['orcamento_atividades'] = orcamento_atividades_list
        
        despesas = Despesa.objects.filter(orcamento = orcamento)
        despesa_list = DespesaSerializer(despesas, many=True).data
        
        orcamento_dict['despesas'] = despesa_list
        
    return orcamento_dict;
    
def serializar_fase_atividade(fase_atividades):
    '''
        Utilizado em outros locais além desse
    '''
    fase_atividade_list = []
    
    if fase_atividades:
        fase_atividade_list = FaseAtividadeSerializer(fase_atividades, many = True).data   
        for i in fase_atividade_list:
            
            if 'data_inicio' in i:
                i['data_inicio'] = serializar_data(i['data_inicio'])
            if 'data_fim' in i:
                i['data_fim'] = serializar_data(i['data_fim'])
            
            atividades = Atividade.objects.filter(fase_atividade__id = i['id'])
            
            atividade_list = []
            
            if atividades:
                atividade_list = AtividadeSerializer(atividades, many=True).data
                for a in atividade_list:
                    if 'data_inicio' in a:
                        a['data_inicio'] = serializar_data(a['data_inicio'])
                    if 'data_fim' in a:
                        a['data_fim'] = serializar_data(a['data_fim'])

                    atividade_profissionais = AtividadeProfissional.objects.filter(atividade__id = a['id'])
                    
                    if atividade_profissionais:
                        a['atividadeprofissionais'] = AtividadeProfissionalSerializer(atividade_profissionais, many=True).data
                    
            i['atividades'] = atividade_list
            
    return fase_atividade_list

class DemandaDetail(APIView):
   
    def get(self, request, demanda_id, format=None):
        data = serializarDemanda(demanda_id)
        return Response(data)
        
    def salvar_proposta(self, propostas, demanda):
        for i in propostas:
            if 'remover' not in i or i['remover'] is False:
                if 'data_recimento_solicitacao' in i and i['data_recimento_solicitacao'] is not None:
                    proposta = Proposta(**i)
                    proposta.demanda = demanda
                    data_string = i['data_recimento_solicitacao']
                    proposta.data_recimento_solicitacao = converter_string_para_data(data_string)
                    if 'data_limite_entrega' in i:
                        data_string = i['data_limite_entrega']
                        proposta.data_limite_entrega = converter_string_para_data(data_string)
                    if 'data_real_entrega' in i:
                        data_string = i['data_real_entrega']
                        proposta.data_real_entrega = converter_string_para_data(data_string)
                    if 'data_aprovacao' in i:
                        data_string = i['data_aprovacao']
                        proposta.data_aprovacao = converter_string_para_data(data_string)
                    proposta.save()
            else:
                if 'id' in i:
                    proposta = Proposta.objects.get(pk=i['id'])
                    proposta.delete()
    
    def salvar_observacoes(self, observacoes, demanda):
        for i in observacoes:
            if 'remover' not in i or i['remover'] is False:
                if ('observacao' in i and i['observacao'] is not None and 'data_observacao' in i and i['data_observacao'] is not None):
                    observacao = Observacao(**i)
                    observacao.demanda = demanda
                    observacao.data_observacao = converter_string_para_data(i['data_observacao'])
                    observacao.save()
            else:
                if 'id' in i:
                    observacao = Observacao.objects.get(pk=i['id'])
                    observacao.delete()

    def salvar_ocorrencias(self, ocorrencias, demanda):
        for i in ocorrencias:
            if 'remover' not in i or i['remover'] is False:
                if 'tipo_ocorrencia' in i and i['tipo_ocorrencia'] is not None:
                    
                    if 'show' in i:
                        del i['show']
                    
                    responsavel = None
                    if 'responsavel' in i:
                        if i['responsavel'] is not None and 'id' in i['responsavel']:
                            responsavel = i['responsavel']
                            responsavel = PessoaFisica.objects.get(pk=responsavel['id'])
                        del i['responsavel']
                    ocorrencia = Ocorrencia(**i)
                    ocorrencia.demanda = demanda
                    if responsavel is not None:
                        ocorrencia.responsavel = responsavel
                    if 'data_solicitacao' in i:
                        data_string = i['data_solicitacao']
                        ocorrencia.data_solicitacao = converter_string_para_data(data_string)
                    if 'data_prevista_conclusao' in i:
                        data_string = i['data_prevista_conclusao']
                        ocorrencia.data_prevista_conclusao = converter_string_para_data(data_string)
                    ocorrencia.save()
            else:
                if 'id' in i:
                    ocorrencia = Ocorrencia.objects.get(pk=i['id'])
                    ocorrencia.delete()

    def salvar_orcamento(self, orcamento_dict, demanda):
        
        centro_custo = None
        if 'centro_custo' in orcamento_dict:
            if orcamento_dict['centro_custo']:
                centro_custo = orcamento_dict['centro_custo']
                centro_custo = CentroCusto.objects.get(pk=centro_custo['id'])
            del orcamento_dict['centro_custo']
        
        fases_list= None
        if 'orcamento_fases' in orcamento_dict:
            if orcamento_dict['orcamento_fases']:
                fases_list = orcamento_dict['orcamento_fases']
            del orcamento_dict['orcamento_fases']
            
        orcamento_atividades = None
        if 'orcamento_atividades' in orcamento_dict:
            if orcamento_dict['orcamento_atividades']:
                orcamento_atividades = orcamento_dict['orcamento_atividades']
            del orcamento_dict['orcamento_atividades']
            
        despesas = None
        if 'despesas' in orcamento_dict:
            if orcamento_dict['despesas']:
                despesas = orcamento_dict['despesas']
            del orcamento_dict['despesas']
                
        valor_hora_orcamento = None
        if 'valor_hora_orcamento' in orcamento_dict and orcamento_dict['valor_hora_orcamento']:
            if 'id' in orcamento_dict['valor_hora_orcamento']:
                valor_hora_orcamento = ValorHora.objects.get(pk=orcamento_dict['valor_hora_orcamento']['id'])
            del orcamento_dict['valor_hora_orcamento']
                
        orcamento = Orcamento(**orcamento_dict)
        orcamento.total_orcamento = converter_string_para_float(orcamento.total_orcamento)
        orcamento.imposto_devidos = orcamento.imposto_devidos
        orcamento.total_despesas = converter_string_para_float(orcamento.total_despesas)
        orcamento.valor_desejado = converter_string_para_float(orcamento.valor_desejado)
        orcamento.valor_projetado = converter_string_para_float(orcamento.valor_projetado)
        orcamento.valor_proposto = converter_string_para_float(orcamento.valor_proposto)
        orcamento.valor_hora_orcamento = valor_hora_orcamento
        orcamento.demanda = demanda
        orcamento.centro_custo = centro_custo
        orcamento.save();
        
        self.salvar_orcamento_atividades(orcamento_atividades, orcamento)
        self.salvar_despesas(despesas, orcamento);
        
        if fases_list is not None:    
            for f in fases_list:
                if 'remover' not in f or f['remover'] is False:
                    if 'valor_total' in f and f['valor_total']:
                        itens_fase = None
                        if 'itensfase' in f:
                            itens_fase = f['itensfase']
                            del f['itensfase']
                        
                        fase = None
                        if 'fase' in f:
                            if f['fase'] is not None and 'id' in f['fase'] and f['fase']['id']:
                                fase = Fase.objects.get(pk=f['fase']['id'])
                            del f['fase']
                            
                        orcamento_fase = OrcamentoFase(**f)
                        orcamento_fase.valor_total = converter_string_para_float(orcamento_fase.valor_total)
                        orcamento_fase.fase = fase
                        orcamento_fase.orcamento = orcamento
                        orcamento_fase.save()
                         
                        if itens_fase is not None:
                            for i in itens_fase:
                                
                                if 'remover' not in i or i['remover'] is False:
                                    
                                    valor_hora = None
                                    if 'valor_hora' in i:
                                        valor_hora = ValorHora.objects.get(pk=i['valor_hora']['id'])
                                        del i['valor_hora']
                                        
                                    item_fase = ItemFase(**i)
                                    item_fase.valor_selecionado = converter_string_para_float(item_fase.valor_selecionado)
                                    item_fase.valor_total = converter_string_para_float(item_fase.valor_total)
                                    item_fase.valor_hora = valor_hora
                                    item_fase.orcamento_fase = orcamento_fase
                                    item_fase.save()
                                    
                                elif 'id' in i:
                                    item_fase = ItemFase.objects.get(pk=i['id'])
                                    item_fase.delete()
                                
                elif 'id' in f:
                    orcamento_fase = OrcamentoFase.objects.get(pk=f['id'])
                    orcamento_fase.delete()
    
    def salvar_despesas(self, despesas, orcamento):
        if despesas:
            for i in despesas:
                if ('descricao' in i and i['descricao'] and
                    'valor' in i and i['valor']):
                    despesa = Despesa(**i)
                    despesa.valor = converter_string_para_float(despesa.valor)
                    despesa.orcamento = orcamento
                    despesa.save()
                elif 'id' in i:
                    despesa = Despesa.objects.get(pk=i['id'])
                    despesa.delete()
    
    def salvar_orcamento_atividades(self,orcamento_atividades, orcamento):
        
        if orcamento_atividades:
            for i in orcamento_atividades:
                
                if ('fase' in i and i['fase'] and 
                    'descricao' in i and i['descricao'] and 
                    ('remover' not in i or i['remover'] is False)):
                
                    fase = None
                    if 'fase' in i:
                        if i['fase']:
                            fase = Fase.objects.get(pk=i['fase']['id'])
                        del i['fase']
                        
                    colunas = None
                    if 'colunas' in i:
                        if i['colunas']:
                            colunas = i['colunas']
                        del i['colunas']
                    
                    orcamento_atividade = OrcamentoAtividade(**i)
                    orcamento_atividade.orcamento = orcamento
                    orcamento_atividade.fase = fase
                    orcamento_atividade.save()
        
                    perfil_atividades = PerfilAtividade.objects.filter(orcamento_atividade__id = orcamento_atividade.id)
                    if perfil_atividades:
                        for perfil_atividade in perfil_atividades:
                            perfil_atividade.delete()
                    if colunas:
                        for id_valorhora, horas in colunas.items():
                            perfil_atividade = PerfilAtividade()
                            perfil_atividade.orcamento_atividade = orcamento_atividade
                            perfil_atividade.horas = horas['horas']
                            valor_hora = ValorHora.objects.get(pk=id_valorhora)
                            perfil_atividade.perfil = valor_hora
                            perfil_atividade.save()
        
                elif 'id' in i:
                    orcamento_atividade = OrcamentoAtividade.objects.get(pk=i['id'])
                    orcamento_atividade.delete();
    
    def calcular_estatisticas_demanda(self, demanda):
        
        atividade_profissionais = AtividadeProfissional.objects.filter(atividade__fase_atividade__demanda = demanda)
        
        for atividade_profissional in atividade_profissionais:
            
            alocacoes_horas = AlocacaoHoras.objects.filter(atividade_profissional = atividade_profissional)
            if alocacoes_horas:
                total_milisegundos = 0
    
                for i in alocacoes_horas:
                    total_milisegundos += i.horas_alocadas_milisegundos
                        
                ultimo_percentual = alocacoes_horas[len(alocacoes_horas) - 1].percentual_concluido if alocacoes_horas[len(alocacoes_horas) - 1].percentual_concluido else 0;
                
                atividade_profissional.horas_alocadas_milisegundos = total_milisegundos
                quantidade_horas_milisegundos = atividade_profissional.quantidade_horas * 60 * 60 * 1000
                percentual_calculado = (atividade_profissional.horas_alocadas_milisegundos * 100) / quantidade_horas_milisegundos
                if percentual_calculado > 100:
                    percentual_calculado = 100
                atividade_profissional.percentual_calculado = percentual_calculado
                atividade_profissional.percentual_concluido = ultimo_percentual
                atividade_profissional.save()
                
        #Calcular percentual atividade
        atividades = Atividade.objects.filter(fase_atividade__demanda=demanda)
        if atividades:
            for atividade in atividades:
                atividades_profissionais = AtividadeProfissional.objects.filter(atividade=atividade)
                if atividades_profissionais:
                    percentual_calculado = sum((a.percentual_calculado if a.percentual_calculado else 0) for a in atividades_profissionais) / len(atividades_profissionais)
                    percentual_concluido = sum((a.percentual_concluido if a.percentual_concluido else 0) for a in atividades_profissionais) / len(atividades_profissionais)
                    atividade.percentual_calculado = percentual_calculado
                    atividade.percentual_concluido = percentual_concluido
                    atividade.save()
                    
        #calcular percentual fase_atividade
        fase_atividades = FaseAtividade.objects.filter(demanda=demanda)
        if fase_atividades:
            for fase_atividade in fase_atividades:
                atividades = Atividade.objects.filter(fase_atividade=fase_atividade)
                if atividades:
                    percentual_calculado = sum((a.percentual_calculado if a.percentual_calculado else 0) for a in atividades) / len(atividades)
                    percentual_concluido = sum((a.percentual_concluido if a.percentual_concluido else 0) for a in atividades) / len(atividades)
                    fase_atividade.percentual_calculado = percentual_calculado
                    fase_atividade.percentual_concluido = percentual_concluido
                    fase_atividade.save()
                
                
        fase_atividades = FaseAtividade.objects.filter(demanda=demanda)
        if fase_atividades:
            percentual_calculado = sum((a.percentual_calculado if a.percentual_calculado else 0) for a in fase_atividades) / len(fase_atividades)
            percentual_concluido = sum((a.percentual_concluido if a.percentual_concluido else 0) for a in fase_atividades) / len(fase_atividades)
            demanda.percentual_calculado = percentual_calculado
            demanda.percentual_concluido = percentual_concluido
            demanda.save()    
    
    def salvar_fase_atividades(self, fase_atividades, demanda):
        
        if fase_atividades:
            for i in fase_atividades:
                if 'fase' in i and i['fase'] and 'data_inicio' in i and 'data_fim' in i and ('remover' not in i or i['remover'] is False):
                    
                    atividades = None
                    if 'atividades' in i:
                        if i['atividades']:
                            atividades = i['atividades']
                        del i['atividades']
                    
                    fase = None
                    if 'fase' in i:
                        if i['fase'] and 'id' in i['fase']:
                            fase = Fase.objects.get(pk=i['fase']['id'])
                        del i['fase']
                    
                    responsavel = None
                    if 'responsavel' in i:
                        if i['responsavel'] and 'id' in i['responsavel'] and i['responsavel']['id'] is not None:
                            responsavel = PessoaFisica.objects.get(pk=i['responsavel']['id'])
                        del i['responsavel']
                            
                    fase_atividade = FaseAtividade(**i)
                    fase_atividade.data_inicio = converter_string_para_data(fase_atividade.data_inicio)
                    fase_atividade.data_fim = converter_string_para_data(fase_atividade.data_fim)
                    fase_atividade.fase = fase
                    fase_atividade.responsavel = responsavel
                    fase_atividade.demanda = demanda
                    fase_atividade.save()
                    
                    self.salvar_atividade(atividades, fase_atividade)
                    
                elif 'id' in i:
                    fase_atividade = FaseAtividade.objects.get(pk=i['id'])
                    fase_atividade.delete();
        
        pass
    
    def salvar_atividade(self, atividade_list, fase_atividade):
        if atividade_list:
            for i in atividade_list:
                if 'descricao' in i and 'data_inicio' in i and 'data_fim' in i and ('remover' not in i or i['remover'] is False):
    
                    atividade_profissionais = None
                    if 'atividadeprofissionais' in i:
                        atividade_profissionais = i['atividadeprofissionais']
                        del i['atividadeprofissionais']
                    
                    if 'data_inicio_string' in i:
                        del i['data_inicio_string']
                        
                    if 'data_fim_string' in i:
                        del i['data_fim_string']
                    
                    atividade = Atividade(**i)
                    atividade.fase_atividade = fase_atividade
                    atividade.data_inicio = converter_string_para_data(atividade.data_inicio)
                    atividade.data_fim = converter_string_para_data(atividade.data_fim)
                    atividade.save()
                    
                    self.salvar_atividade_profissionais(atividade_profissionais, atividade)
                    
                elif 'id' in i:
                    atividade = Atividade.objects.get(pk=i['id'])
                    atividade.delete();
                
    def salvar_atividade_profissionais(self, atividade_profissionais, atividade):
        if atividade_profissionais:
            for i in atividade_profissionais:
                if 'pessoa_fisica' in i and i['pessoa_fisica'] and 'id' in i['pessoa_fisica'] and 'quantidade_horas' in i and ('remover' not in i or i['remover'] is False):
                    
                    pessoa_fisica = PessoaFisica.objects.get(pk=i['pessoa_fisica']['id'])
                    del i['pessoa_fisica']
                    
                    if 'quantidade_horas_formatada' in i:
                        del i['quantidade_horas_formatada']
                        
                    if 'horas_alocadas' in i:
                        del i['horas_alocadas']
                    
                    atividade_profissional = AtividadeProfissional(**i)
                    atividade_profissional.atividade = atividade
                    atividade_profissional.pessoa_fisica = pessoa_fisica
                    atividade_profissional.save()
                    
                elif 'id' in i:
                    atividade_profissional = AtividadeProfissional.objects.get(pk=i['id'])
                    atividade_profissional.delete()
    
    def salvar_parcelas(self, parcela_list, demanda):
        
        if parcela_list:
            for i in parcela_list:
                if 'remover' not in i or i['remover'] == False:
                    
                    valor_parcela = None
                    if 'valor_parcela' in i:
                        valor_parcela = converter_string_para_float(i['valor_parcela'])
                        del i['valor_parcela']
                    
                    data_previsto_parcela = None
                    if 'data_previsto_parcela' in i:
                        data_previsto_parcela = converter_string_para_data(i['data_previsto_parcela'])
                        del i['data_previsto_parcela']
                    
                    medicao_list = None
                    if 'medicoes' in i:
                        medicao_list = i['medicoes']
                        del i['medicoes']  
                    
                    if 'demanda' in i:
                        del i['demanda']  
                    
                    parcela = Parcela(**i)
                    parcela.valor_parcela = valor_parcela
                    parcela.data_previsto_parcela = data_previsto_parcela
                    parcela.demanda = demanda
                    parcela.tipo_parcela = demanda.tipo_parcela
                    parcela.save()
                    
                    self.gravar_medicoes(parcela, medicao_list)
                    
                elif 'id' in i:
                    parcela = Parcela.objects.get(pk=i['id'])
                    parcela.delete()
                    
                    
    def gravar_medicoes(self, parcelafase, medicoes):
        
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
                    medicao.valor = converter_string_para_float(medicao.valor)   
                    medicao.valor_total = converter_string_para_float(medicao.valor_total)
                    medicao.parcela = parcelafase
                    medicao.save()
                    
                elif 'id' in i:
                    medicao = Medicao.objects.get(pk=i['id'])
                    medicao.delete()
         
        return medicao_list   
        
    def post(self, request, format=None):
        
        data = request.data
        
        cliente = data['cliente']
        cliente = PessoaJuridica.objects.get(pk=cliente['id'])
        
        unidade_administrativa = data['unidade_administrativa']
        unidade_administrativa = UnidadeAdministrativa.objects.get(pk=unidade_administrativa['id'])
        
        analista_tecnico_responsavel = None
        if 'analista_tecnico_responsavel' in data:
            if data['analista_tecnico_responsavel'] is not None and 'id' in data['analista_tecnico_responsavel']:
                analista_tecnico_responsavel = data['analista_tecnico_responsavel']
                analista_tecnico_responsavel = PessoaFisica.objects.get(pk=analista_tecnico_responsavel['id'])
            del data['analista_tecnico_responsavel']
            
        responsavel = None
        if 'responsavel' in data:
            if data['responsavel'] is not None and 'id' in data['responsavel']:
                responsavel = data['responsavel']
                responsavel = PessoaFisica.objects.get(pk=responsavel['id'])
            del data['responsavel']
        
        natureza_demanda = None
        if 'natureza_demanda' in data:
            if data['natureza_demanda'] is not None and 'id' in data['natureza_demanda']:
                natureza_demanda = NaturezaDemanda.objects.get(pk=data['natureza_demanda']['id'])
            del data['natureza_demanda']
        
        propostas = data['propostas']
        observacoes = data['observacoes']
        ocorrencias = data['ocorrencias']
        orcamento = data['orcamento']
        
        fase_atividades = None
        if 'fase_atividades' in data:
            if data['fase_atividades']:
                fase_atividades = data['fase_atividades']
            del data['fase_atividades']
            
        if 'parcelas' in data:
            del data['parcelas']
        
        del data['cliente']
        del data['propostas']
        del data['observacoes']
        del data['ocorrencias']
        del data['orcamento']
        del data['unidade_administrativa']

        demanda = Demanda(**data)
        demanda.cliente = cliente
        demanda.unidade_administrativa = unidade_administrativa
       
        if 'data_aprovacao_demanda' in data:
            data_string = data['data_aprovacao_demanda']
            demanda.data_aprovacao_demanda = converter_string_para_data(data_string)
            
        if 'data_inicio' in data:
            data_string = data['data_inicio']
            demanda.data_inicio = converter_string_para_data(data_string)
            
        if 'data_fim' in data:
            data_string = data['data_fim']
            demanda.data_fim = converter_string_para_data(data_string)
            
        if 'data_criacao' in data:
            data_string = data['data_criacao']
            demanda.data_criacao = converter_string_para_data(data_string)
            
        demanda.analista_tecnico_responsavel = analista_tecnico_responsavel
        demanda.responsavel = responsavel
        demanda.natureza_demanda = natureza_demanda
            
        demanda.save();
        
        self.salvar_proposta(propostas, demanda)
        self.salvar_observacoes(observacoes, demanda)
        self.salvar_ocorrencias(ocorrencias, demanda)
        self.salvar_orcamento(orcamento, demanda)
        self.salvar_fase_atividades(fase_atividades, demanda)
        
        if demanda.tipo_demanda != 'I':
            self.calcular_estatisticas_demanda(demanda)
        
        return Response(serializarDemanda(demanda.id))
    
    def delete(self, request, demanda_id, format=None):
        demanda = Demanda.objects.get(pk=demanda_id)
        demanda.delete()
        data = DemandaSerializer(demanda).data
        return Response(data)

@api_view(['GET'])
def buscar_atividades_demanda(request, demanda_id, format=None):
    fase_atividades = FaseAtividade.objects.filter(demanda__id=demanda_id)
    list = serializar_fase_atividade(fase_atividades)
    return Response(list)

@api_view(['GET'])
def buscar_total_horas_custo_resultado_por_demanda(request, demanda_id, format=None):
    
    resultado = Orcamento.objects.filter(demanda__id=demanda_id).values('orcamentofase__itemfase__valor_hora__centro_resultado__id', 'orcamentofase__itemfase__valor_hora__centro_resultado__nome').annotate(total_horas = Sum('orcamentofase__itemfase__quantidade_horas'))
    return Response(resultado)

@api_view(['GET'])
def buscar_total_horas_orcamento(request, demanda_id, format=None):
    resultado = Orcamento.objects.filter(demanda__id=demanda_id).values('id').annotate(total_horas = Sum('orcamentofase__itemfase__quantidade_horas'))
    return Response(resultado[0])

@api_view(['GET'])
def buscar_total_horas_por_valor_hora(request, demanda_id, format=None):
    resultado = Orcamento.objects.filter(demanda__id=demanda_id).values('orcamentofase__id', 'orcamentofase__fase__descricao', 'orcamentofase__itemfase__valor_hora__id', 'orcamentofase__itemfase__valor_hora__descricao').annotate(total_horas = Sum('orcamentofase__itemfase__quantidade_horas'))
    return Response(resultado)

REGISTROS_POR_PAGINA = 14

@api_view(['POST'])
def buscar_lista_por_parametro(request, format=None):
    
    if request.data:
        arguments = {}
        
        if 'data_inicio' in request.data and request.data['data_inicio']:
            data_inicio = converter_string_para_data(request.data['data_inicio'])
            arguments['data_criacao__gte'] = data_inicio
            
        if 'data_fim' in request.data and request.data['data_fim']:
            data_fim = converter_string_para_data(request.data['data_fim'])
            arguments['data_criacao__lte'] = data_fim
            
        if 'cliente_id' in request.data and request.data['cliente_id']:
            arguments['cliente__id'] = request.data['cliente_id']
            
        if 'nome_demanda' in request.data and request.data['nome_demanda']:
            arguments['nome_demanda__icontains'] = request.data['nome_demanda']
            
        list_status = []
        if 'status' in request.data and request.data['status']:
            for k in request.data['status']:
                if request.data['status'][k]:
                    list_status.append(k)
                    
        list_responsaveis = []
        if 'responsaveis' in request.data and request.data['responsaveis']:
            for k in request.data['responsaveis']:
                if request.data['responsaveis'][k]:
                    list_responsaveis.append(k);
        
        demandas = Demanda.objects.filter(**arguments)
            
        if list_status:
            demandas = demandas.filter(status_demanda__in=list_status)

        if list_responsaveis:
            demandas = demandas.filter(responsavel__id__in=list_responsaveis)
        
        if 'palavra_chave' in request.data and request.data['palavra_chave']:
            if  request.data['palavra_chave'].isdigit():
                palavra_chave = request.data['palavra_chave']
                demandas = demandas.filter(Q(id=palavra_chave)
                            | Q(nome_demanda__icontains=palavra_chave)
                            | Q(faseatividade__atividade__descricao__icontains=palavra_chave)
                            | Q(descricao__icontains=palavra_chave)
                            | Q(cliente__pessoa__nome_razao_social__icontains=palavra_chave)).distinct()
            else:
                palavra_chave = request.data['palavra_chave']
                demandas = demandas.filter(Q(nome_demanda__icontains=palavra_chave)
                            | Q(faseatividade__atividade__descricao__icontains=palavra_chave)
                            | Q(descricao__icontains=palavra_chave)
                            | Q(cliente__pessoa__nome_razao_social__icontains=palavra_chave)).distinct()
        
        if request.data['ordenar'] is False:
            demandas = demandas.order_by('pk')
        else:
            demandas = demandas.order_by('-pk')
            
        pagina = request.data['pagina']
        paginator = Paginator(demandas, REGISTROS_POR_PAGINA)
        total_paginas = paginator.num_pages
        if 'pagina' in request.data:
            if pagina > total_paginas:
                pagina = total_paginas
            demandas = paginator.page(pagina)
        else:
            demandas = paginator.page(1)
        
            
    else:
        demandas = Demanda.objects.all().order_by('-id')
        paginator = Paginator(demandas, REGISTROS_POR_PAGINA)
        demandas = paginator.page(1)
        total_paginas = paginator.num_pages
    
    demandas = DemandaSerializer(demandas, many=True).data
    
    dict = {
       'demandas': demandas,
       'total_paginas': total_paginas 
    }
    
    return Response(dict)

@api_view(['GET'])
def atividade_profissional_possui_alocacao(request, atividade_profissional_id, format=None):
    
    count = AlocacaoHoras.objects.filter(atividade_profissional__id=atividade_profissional_id).count()
    
    context = {
        'possui': (count > 0)
    }
    
    return Response(context)

@api_view(['GET'])
def atividade_possui_alocacao(request, atividade_id, format=None):
    
    count = AlocacaoHoras.objects.filter(atividade_profissional__atividade__id=atividade_id).count()
    
    context = {
        'possui': (count > 0)
    }
    
    return Response(context)



@api_view(['GET'])
def buscar_lista_por_texto(request, texto, format=None):
    demandas = Demanda.objects.filter(nome_demanda__icontains=texto)[:10]
    demandas = DemandaInicialSerializer(demandas, many=True).data
    return Response(demandas)