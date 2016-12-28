from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from demandas.models import Demanda, FaturamentoDemanda, Proposta, Tarefa, Observacao, Ocorrencia,\
    Orcamento, ItemFase, Fase, Atividade, ValorHoraFaturamento
from clientes.models import Cliente
from demandas.serializers import DemandaSerializer, FaturamentoDemandaSerializer, PropostaSerializer, TarefasSerializer,\
    ObservacaoSerializer, OcorrenciaSerializer, OrcamentoSerializer,\
    ItemFaseSerializer, FaseSerializer, AtividadeSerializer, ValorHoraFaturamentoSerializer
from utils.utils import converter_string_para_data, formatar_data, converter_string_para_float
from recursos.models import Funcionario
from cadastros.models import CentroCusto, ValorHora, CentroResultado, UnidadeAdministrativa
from rest_framework.decorators import api_view
from django.db.models.aggregates import Sum
from faturamento.models import Parcela, Medicao, ParcelaFase
from faturamento.serializers import ParcelaSerializer, MedicaoSerializer, ParcelaFaseSerializer

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
    

    def serializarDemanda(self, demanda_id):
        
        demanda = Demanda.objects.get(pk=demanda_id)
        itens_faturamento = FaturamentoDemanda.objects.filter(demanda__id=demanda_id)
        propostas = Proposta.objects.filter(demanda__id=demanda_id)
        tarefas = Tarefa.objects.filter(demanda__id=demanda_id)
        observacoes = Observacao.objects.filter(demanda__id=demanda_id)
        ocorrencias = Ocorrencia.objects.filter(demanda__id=demanda_id)
        orcamentos = Orcamento.objects.filter(demanda__id=demanda_id)
        atividades = Atividade.objects.filter(demanda__id=demanda_id)
        parcelas = Parcela.objects.filter(demanda__id=demanda_id)
        
        data = DemandaSerializer(demanda).data
        
        itens_list = []
        for i in itens_faturamento:
            faturamento_demanda = FaturamentoDemandaSerializer(i).data
            faturamento_demanda['data_envio_aprovacao'] = formatar_data(i.data_envio_aprovacao)
            faturamento_demanda['data_previsto_faturamento'] = formatar_data(i.data_previsto_faturamento)
            faturamento_demanda['data_previsto_pagamento'] = formatar_data(i.data_previsto_pagamento)
            faturamento_demanda['data_pagamento'] = formatar_data(i.data_pagamento)
            faturamento_demanda['data_fatura'] = formatar_data(i.data_fatura)
            
            valor_hora_faturamentos = ValorHoraFaturamento.objects.filter(faturamento_demanda = i)
            valorhoras_list = ValorHoraFaturamentoSerializer(valor_hora_faturamentos, many=True).data
            faturamento_demanda['valorhoras'] = valorhoras_list
            
            itens_list.append(faturamento_demanda)
        
        propostas_list = []
        for i in propostas:
            proposta = PropostaSerializer(i).data
            proposta['data_recimento_solicitacao'] = formatar_data(i.data_recimento_solicitacao)
            proposta['data_limite_entrega'] = formatar_data(i.data_limite_entrega)
            proposta['data_real_entrega'] = formatar_data(i.data_real_entrega)
            proposta['data_aprovacao'] = formatar_data(i.data_aprovacao)
            propostas_list.append(proposta)
            
        tarefas_list = []
        for i in tarefas:
            tarefa = TarefasSerializer(i).data
            tarefa['analise_inicio'] = formatar_data(i.analise_inicio)
            tarefa['analise_fim'] = formatar_data(i.analise_fim)
            tarefa['analise_fim_real'] = formatar_data(i.analise_fim_real)
            tarefa['densenvolvimento_inicio'] = formatar_data(i.densenvolvimento_inicio)
            tarefa['desenvolvimento_fim'] = formatar_data(i.desenvolvimento_fim)
            tarefa['desenvolvimento_fim_real'] = formatar_data(i.desenvolvimento_fim_real)
            tarefa['homologacao_inicio'] = formatar_data(i.homologacao_inicio)
            tarefa['homologacao_fim'] = formatar_data(i.homologacao_fim)
            tarefa['homologacao_fim_real'] = formatar_data(i.homologacao_fim_real)
            tarefa['implantacao_producao'] = formatar_data(i.implantacao_producao)
            tarefas_list.append(tarefa)
            
        observacoes_list = []
        for i in observacoes:
            observacao = ObservacaoSerializer(i).data
            observacao['data_observacao'] = formatar_data(i.data_observacao)
            observacoes_list.append(observacao)
            
        ocorrencias_list = []
        for i in ocorrencias:
            ocorrencia = OcorrenciaSerializer(i).data
            ocorrencia['data_solicitacao'] = formatar_data(i.data_solicitacao)
            ocorrencia['data_prevista_conclusao'] = formatar_data(i.data_prevista_conclusao)
            ocorrencias_list.append(ocorrencia)
            
        orcamento_dict = {}
        if  orcamentos:
            orcamento = orcamentos[0]
            orcamento_dict = OrcamentoSerializer(orcamento).data
            fases = Fase.objects.filter(orcamento = orcamento)
            
            fases_list = []
            for i in fases:
                itens_fase = ItemFase.objects.filter(fase = i)
                intes_fase_list = ItemFaseSerializer(itens_fase, many=True).data
                fase_dict = FaseSerializer(i).data
                fase_dict['itensfase'] = intes_fase_list
                fases_list.append(fase_dict)
                
            orcamento_dict['fases'] = fases_list
        
        atividade_list = []
        if atividades:
            atividade_list = AtividadeSerializer(atividades, many=True).data    
            
        parcelas_list = []
        for i in parcelas:
            
            parcela = ParcelaSerializer(i).data
            parcela['data_previsto_parcela'] = formatar_data(i.data_previsto_parcela)
            
            parcelafase_list = ParcelaFase.objects.filter(parcela = i)
            parcelafaseserializer_list = []
            for pf in parcelafase_list:
                parcelafaseserializer = ParcelaFaseSerializer(pf).data
                medicoes = Medicao.objects.filter(parcela_fase = pf)
                medicao_list = MedicaoSerializer(medicoes, many=True).data
                parcelafaseserializer['medicoes'] = medicao_list
                
                parcelafaseserializer_list.append(parcelafaseserializer)
            parcela['parcelafases'] = parcelafaseserializer_list
                
            parcelas_list.append(parcela)
        
        data['itens_faturamento'] = itens_list
        data['propostas'] = propostas_list
        data['tarefas'] = tarefas_list
        data['observacoes'] = observacoes_list
        data['ocorrencias'] = ocorrencias_list
        data['orcamento'] = orcamento_dict
        data['atividades'] = atividade_list
        data['parcelas'] = parcelas_list
        
        return data

    def get(self, request, demanda_id, format=None):
        data = self.serializarDemanda(demanda_id)
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

    def salvar_item_faturamento(self, itens_faturamento, demanda):
        for i in itens_faturamento:
            if 'remover' not in i or i['remover'] is False:
                if 'descricao' in i and i['descricao'] is not None and 'numero_nota' in i and i['numero_nota'] is not None:
                    
                    valorhoras_list = [] 
                    if 'valorhoras' in i and i['valorhoras'] is not None:
                        valorhoras_list = i['valorhoras']
                        del i['valorhoras']
                    
                    faturamento_demanda = FaturamentoDemanda(**i)
                    faturamento_demanda.demanda = demanda
                    
                    if 'data_envio_aprovacao' in i:
                        data_string = i['data_envio_aprovacao']
                        faturamento_demanda.data_envio_aprovacao = converter_string_para_data(data_string)
                    if 'data_previsto_faturamento' in i:
                        data_string = i['data_previsto_faturamento']
                        faturamento_demanda.data_previsto_faturamento = converter_string_para_data(data_string)
                    if 'data_previsto_pagamento' in i:
                        data_string = i['data_previsto_pagamento']
                        faturamento_demanda.data_previsto_pagamento = converter_string_para_data(data_string)
                    if 'data_pagamento' in i:
                        data_string = i['data_pagamento']
                        faturamento_demanda.data_pagamento = converter_string_para_data(data_string)
                    if 'data_fatura' in i:
                        data_string = i['data_fatura']
                        faturamento_demanda.data_fatura = converter_string_para_data(data_string)
                    faturamento_demanda.save()
                    
                    self.salvar_valor_hora_faturamento(faturamento_demanda, valorhoras_list)
                    
            else:
                if 'id' in i:
                    faturamento_demanda = FaturamentoDemanda.objects.get(pk=i['id'])
                    faturamento_demanda.delete()

    def salvar_valor_hora_faturamento(self, faturamento_demanda, valorhoras_list):
        
        for t in valorhoras_list:
            if 'remover' not in t or t['remover'] is False:
                
                valor_hora = None
                if 'valor_hora' in t:
                    valor_hora = ValorHora.objects.get(pk=t['valor_hora']['id'])
                    del t['valor_hora']
                
                valor_hora_faturamento = ValorHoraFaturamento(**t)
                valor_hora_faturamento.valor_hora = valor_hora
                valor_hora_faturamento.valor = converter_string_para_float(valor_hora_faturamento.valor)
                valor_hora_faturamento.faturamento_demanda = faturamento_demanda
                valor_hora_faturamento.save()
                
            elif 'id' in t:
                valor_hora_faturamento = ValorHoraFaturamento.objects.get(pk=t['id'])
                valor_hora_faturamento.delete()

    
    def salvar_tarefa(self, tarefas, demanda):
        for i in tarefas:
            if 'remover' not in i or i['remover'] is False:
                if ('descricao' in i and i['descricao'] is not None and 'analista_tecnico_responsavel' in i and i['analista_tecnico_responsavel'] is not None and 
                    'responsavel' in i and i['responsavel'] is not None):
                    
                    if 'show' in i:
                        del i['show']
                    
                    analista_tecnico_responsavel = None
                    if 'analista_tecnico_responsavel' in i:
                        if i['analista_tecnico_responsavel'] is not None and 'id' in i['analista_tecnico_responsavel']:
                            analista_tecnico_responsavel = i['analista_tecnico_responsavel']
                            analista_tecnico_responsavel = Funcionario.objects.get(pk=analista_tecnico_responsavel['id'])
                        del i['analista_tecnico_responsavel']
                        
                    responsavel = None
                    if 'responsavel' in i:
                        if i['responsavel'] is not None and 'id' in i['responsavel']:
                            responsavel = i['responsavel']
                            responsavel = Funcionario.objects.get(pk=responsavel['id'])
                        del i['responsavel']
                    
                    tarefa = Tarefa(**i)
                    tarefa.demanda = demanda
                    
                    if analista_tecnico_responsavel is not None:
                        tarefa.analista_tecnico_responsavel = analista_tecnico_responsavel
                    
                    if responsavel is not None:
                        tarefa.responsavel = responsavel
                    
                    if 'analise_inicio' in i:
                        data_string = i['analise_inicio']
                        tarefa.analise_inicio = converter_string_para_data(data_string)
                    if 'analise_fim' in i:
                        data_string = i['analise_fim']
                        tarefa.analise_fim = converter_string_para_data(data_string)
                    if 'analise_fim_real' in i:
                        data_string = i['analise_fim_real']
                        tarefa.analise_fim_real = converter_string_para_data(data_string)
                    if 'densenvolvimento_inicio' in i:
                        data_string = i['densenvolvimento_inicio']
                        tarefa.densenvolvimento_inicio = converter_string_para_data(data_string)
                    if 'desenvolvimento_fim' in i:
                        data_string = i['desenvolvimento_fim']
                        tarefa.desenvolvimento_fim = converter_string_para_data(data_string)
                    if 'desenvolvimento_fim_real' in i:
                        data_string = i['desenvolvimento_fim_real']
                        tarefa.desenvolvimento_fim_real = converter_string_para_data(data_string)
                    if 'homologacao_inicio' in i:
                        data_string = i['homologacao_inicio']
                        tarefa.homologacao_inicio = converter_string_para_data(data_string)
                    if 'homologacao_fim' in i:
                        data_string = i['homologacao_fim']
                        tarefa.homologacao_fim = converter_string_para_data(data_string)
                    if 'homologacao_fim_real' in i:
                        data_string = i['homologacao_fim_real']
                        tarefa.homologacao_fim_real = converter_string_para_data(data_string)
                    if 'implantacao_producao' in i:
                        data_string = i['implantacao_producao']
                        tarefa.implantacao_producao = converter_string_para_data(data_string)
                    tarefa.save()
            else:
                if 'id' in i:
                    tarefa = Tarefa.objects.get(pk=i['id'])
                    tarefa.delete()

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
                            responsavel = Funcionario.objects.get(pk=responsavel['id'])
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
        
        orcamento = Orcamento(**orcamento_dict)
        orcamento.total_orcamento = converter_string_para_float(orcamento.total_orcamento)
        orcamento.demanda = demanda
        orcamento.centro_custo = centro_custo
        orcamento.save();
        
        if fases_list is not None:    
            for f in fases_list:
                if 'remover' not in f or f['remover'] is False:
                    if 'descricao' in f and f['descricao'] and 'valor_total' in f and f['valor_total']:
                        itens_fase = None
                        if 'itensfase' in f:
                            itens_fase = f['itensfase']
                            del f['itensfase']
                            
                        fase = Fase(**f)
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
    
    def salvar_atividade(self, atividade_list, demanda):
        
        for i in atividade_list:
            if 'remover' not in i or i['remover'] is False:
                if 'titulo' in i:
                    responsavel = None
                    if 'responsavel' in i:
                        responsavel = Funcionario.objects.get(pk=i['responsavel']['id'])
                        del i['responsavel']
                    
                    centro_resultado = None
                    if 'centro_resultado' in i:
                        centro_resultado = CentroResultado.objects.get(pk=i['centro_resultado']['id'])
                        del i['centro_resultado']
                    
                    atividade = Atividade(**i)
                    atividade.responsavel = responsavel
                    atividade.centro_resultado = centro_resultado
                    atividade.demanda = demanda
                    
                    atividade.save()
                
            elif 'id' in i:
                atividade = Atividade.objects.get(pk=i['id'])
                atividade.delete();
                
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
        cliente = Cliente.objects.get(pk=cliente['id'])
        
        unidade_administrativa = data['unidade_administrativa']
        unidade_administrativa = UnidadeAdministrativa.objects.get(pk=unidade_administrativa['id'])
        
        itens_faturamento = data['itens_faturamento']
        propostas = data['propostas']
        tarefas = data['tarefas']
        observacoes = data['observacoes']
        ocorrencias = data['ocorrencias']
        orcamento = data['orcamento']
        atividades = data['atividades']
        
        parcelas = None
        if 'parcelas' in data:
            parcelas = data['parcelas']
            del data['parcelas']
        
        del data['cliente']
        del data['itens_faturamento']
        del data['propostas']
        del data['tarefas']
        del data['observacoes']
        del data['ocorrencias']
        del data['orcamento']
        del data['atividades']
        del data['unidade_administrativa']

        demanda = Demanda(**data)
        demanda.cliente = cliente
        demanda.unidade_administrativa = unidade_administrativa
       
        if 'data_aprovacao_demanda' in data:
            data_string = data['data_aprovacao_demanda']
            demanda.data_aprovacao_demanda = converter_string_para_data(data_string)
            
        demanda.save();
        
        self.salvar_tarefa(tarefas, demanda)
        self.salvar_proposta(propostas, demanda)
        self.salvar_item_faturamento(itens_faturamento, demanda)
        self.salvar_observacoes(observacoes, demanda)
        self.salvar_ocorrencias(ocorrencias, demanda)
        self.salvar_orcamento(orcamento, demanda)
        self.salvar_atividade(atividades, demanda)
        self.salvar_parcelas(parcelas, demanda)
        
        return Response(self.serializarDemanda(demanda.id))
    
    def delete(self, request, demanda_id, format=None):
        
        demanda = Demanda.objects.get(pk=demanda_id)
        faturamento_demanda =  FaturamentoDemanda.objects.filter(demanda=demanda)
        
        for i in faturamento_demanda:
            i.delete()
            
        demanda.delete()
        
        data = DemandaSerializer(demanda).data
        
        itens = []
        
        for i in faturamento_demanda:
            faturamento_demanda = FaturamentoDemandaSerializer(i).data
            faturamento_demanda['data'] = formatar_data(i.data)
            faturamento_demanda['data_envio_aprovacao'] = formatar_data(i.data_envio_aprovacao)
            faturamento_demanda['data_aprovacao_fatura'] = formatar_data(i.data_aprovacao_fatura)
            faturamento_demanda['data_fatura'] = formatar_data(i.data_fatura)
            itens.append(faturamento_demanda)
            
        data['itens_faturamento'] = itens
        
        return Response(data)
        
        return self.get(request, demanda_id, format=None)
    

@api_view(['GET'])
def buscar_total_horas_custo_resultado_por_demanda(request, demanda_id, format=None):
    
    resultado = Orcamento.objects.filter(demanda__id=demanda_id).values('fase__itemfase__valor_hora__centro_resultado__id', 'fase__itemfase__valor_hora__centro_resultado__nome').annotate(total_horas = Sum('fase__itemfase__quantidade_horas'))
    return Response(resultado)

@api_view(['GET'])
def buscar_total_horas_orcamento(request, demanda_id, format=None):
    resultado = Orcamento.objects.filter(demanda__id=demanda_id).values('id').annotate(total_horas = Sum('fase__itemfase__quantidade_horas'))
    return Response(resultado[0])

@api_view(['GET'])
def buscar_total_horas_por_valor_hora(request, demanda_id, format=None):
    resultado = Orcamento.objects.filter(demanda__id=demanda_id).values('fase__itemfase__valor_hora__id', 'fase__itemfase__valor_hora__descricao').annotate(total_horas = Sum('fase__itemfase__quantidade_horas'))
    return Response(resultado)
    