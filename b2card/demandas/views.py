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
    OrcamentoAtividade, PerfilAtividade, AtividadeProfissional, FaseAtividade
from demandas.serializers import DemandaSerializer, PropostaSerializer, \
    ObservacaoSerializer, OcorrenciaSerializer, OrcamentoSerializer, \
    ItemFaseSerializer, AtividadeSerializer, \
    OrcamentoFaseSerializer, OrcamentoAtividadeSerializer, \
    AtividadeProfissionalSerializer, FaseAtividadeSerializer
from faturamento.models import Parcela, Medicao, ParcelaFase
from faturamento.serializers import ParcelaSerializer, MedicaoSerializer, ParcelaFaseSerializer
from utils.utils import converter_string_para_data, formatar_data, converter_string_para_float,\
    serializarDemanda
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
        if 'fases' in orcamento_dict:
            if orcamento_dict['fases']:
                fases_list = orcamento_dict['fases']
            del orcamento_dict['fases']
            
        orcamento_atividades = None
        if 'orcamento_atividades' in orcamento_dict:
            if orcamento_dict['orcamento_atividades']:
                orcamento_atividades = orcamento_dict['orcamento_atividades']
            del orcamento_dict['orcamento_atividades']
        
        orcamento = Orcamento(**orcamento_dict)
        orcamento.total_orcamento = converter_string_para_float(orcamento.total_orcamento)
        orcamento.demanda = demanda
        orcamento.centro_custo = centro_custo
        orcamento.save();
        
        self.salvar_orcamento_atividades(orcamento_atividades, orcamento)
        
        if fases_list is not None:    
            for f in fases_list:
                if 'remover' not in f or f['remover'] is False:
                    if 'descricao' in f and f['descricao'] and 'valor_total' in f and f['valor_total']:
                        itens_fase = None
                        if 'itensfase' in f:
                            itens_fase = f['itensfase']
                            del f['itensfase']
                            
                        fase = OrcamentoFase(**f)
                        fase.valor_total = converter_string_para_float(fase.valor_total)
                        fase.orcamento = orcamento
                        fase.save()
                         
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
                                    item_fase.fase = fase
                                    item_fase.save()
                                    
                                elif 'id' in i:
                                    item_fase = ItemFase.objects.get(pk=i['id'])
                                    item_fase.delete()
                                
                elif 'id' in f:
                    fase = Fase.objects.get(pk=f['id'])
                    fase.delete()
    
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
        fase_atividades = data['fase_atividades']
        
        if 'parcelas' in data:
            del data['parcelas']
        
        del data['cliente']
        del data['propostas']
        del data['observacoes']
        del data['ocorrencias']
        del data['orcamento']
        del data['unidade_administrativa']
        del data['fase_atividades']

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
        
        return Response(serializarDemanda(demanda.id))
    
    def delete(self, request, demanda_id, format=None):
        demanda = Demanda.objects.get(pk=demanda_id)
        demanda.delete()
        data = DemandaSerializer(demanda).data
        return Response(data)

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
    resultado = Orcamento.objects.filter(demanda__id=demanda_id).values('orcamentofase__id', 'orcamentofase__descricao', 'orcamentofase__itemfase__valor_hora__id', 'orcamentofase__itemfase__valor_hora__descricao').annotate(total_horas = Sum('orcamentofase__itemfase__quantidade_horas'))
    return Response(resultado)

REGISTROS_POR_PAGINA = 15

@api_view(['POST'])
def buscar_lista_por_parametro(request, format=None):
    
    if request.data:
        arguments = {}
        
        if 'data_inicio' in request.data:
            data_inicio = converter_string_para_data(request.data['data_inicio'])
            arguments['data_criacao__gte'] = data_inicio
            
        if 'data_fim' in request.data:
            data_fim = converter_string_para_data(request.data['data_fim'])
            arguments['data_criacao__lte'] = data_fim
            
        if 'cliente_id' in request.data:
            arguments['cliente__id'] = request.data['cliente_id']
            
        if 'status' in request.data:
            arguments['status_demanda'] = request.data['status']
            
        demandas = Demanda.objects.filter(**arguments).order_by('-id')
        if 'palavra_chave' in request.data:
            palavra_chave = request.data['palavra_chave']
            demandas = demandas.filter(Q(id=palavra_chave)
                            | Q(nome_demanda__icontains=palavra_chave)
                            | Q(faseatividade__atividade__descricao__icontains=palavra_chave)
                            | Q(descricao__icontains=palavra_chave)
                            | Q(cliente__pessoa__nome_razao_social__icontains=palavra_chave)).distinct()
            
        
        pagina = request.data['pagina']
        paginator = Paginator(demandas, REGISTROS_POR_PAGINA)
        if 'pagina' in request.data:
            demandas = paginator.page(pagina)
        else:
            demandas = paginator.page(1)
        total_paginas = paginator.num_pages
            
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