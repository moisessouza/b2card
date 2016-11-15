from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from demandas.models import Demanda, FaturamentoDemanda, Proposta, Tarefa, Observacao, Ocorrencia,\
    TipoValorHoraFaturamento
from clientes.models import Cliente, TipoValorHora, CentroResultado
from demandas.serializers import DemandaSerializer, FaturamentoDemandaSerializer, PropostaSerializer, TarefasSerializer,\
    ObservacaoSerializer, OcorrenciaSerializer, TipoValorHoraFaturamentoSerializer
from utils.utils import converter_string_para_data, formatar_data
from recursos.models import Funcionario

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
        
        data = DemandaSerializer(demanda).data
        
        data['data_aprovacao_demanda'] = formatar_data(demanda.data_aprovacao_demanda)

        itens_list = []
        for i in itens_faturamento:
            faturamento_demanda = FaturamentoDemandaSerializer(i).data
            faturamento_demanda['data'] = formatar_data(i.data)
            faturamento_demanda['data_envio_aprovacao'] = formatar_data(i.data_envio_aprovacao)
            faturamento_demanda['data_aprovacao_fatura'] = formatar_data(i.data_aprovacao_fatura)
            faturamento_demanda['data_fatura'] = formatar_data(i.data_fatura)
            
            tipo_valor_hora_faturamento_demanda_list = TipoValorHoraFaturamento.objects.filter(faturamento_demanda=i)
            
            tipo_valor_hora_faturamento_demanda_list_data = []            
            for t in tipo_valor_hora_faturamento_demanda_list:
                tipo_valor_hora_faturamento_demanda = TipoValorHoraFaturamentoSerializer(t).data
                tipo_valor_hora_faturamento_demanda_list_data.append(tipo_valor_hora_faturamento_demanda)
            
            faturamento_demanda['tipovalorhoras'] = tipo_valor_hora_faturamento_demanda_list_data
            
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
        
        data['itens_faturamento'] = itens_list
        data['propostas'] = propostas_list
        data['tarefas'] = tarefas_list
        data['observacoes'] = observacoes_list
        data['ocorrencias'] = ocorrencias_list
        
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
                if 'descricao' in i and i['descricao'] is not None:
                    
                    tipovalorhoras_list = [] 
                    if 'tipovalorhoras' in i and i['tipovalorhoras'] is not None:
                        tipovalorhoras_list = i['tipovalorhoras']
                        del i['tipovalorhoras']
                    
                    faturamento_demanda = FaturamentoDemanda(**i)
                    faturamento_demanda.demanda = demanda
                    
                    if 'data' in i:
                        data_string = i['data']
                        faturamento_demanda.data = converter_string_para_data(data_string)
                    if 'data_envio_aprovacao' in i:
                        data_string = i['data_envio_aprovacao']
                        faturamento_demanda.data_envio_aprovacao = converter_string_para_data(data_string)
                    if 'data_aprovacao_fatura' in i:
                        data_string = i['data_aprovacao_fatura']
                        faturamento_demanda.data_aprovacao_fatura = converter_string_para_data(data_string)
                    if 'data_fatura' in i:
                        data_string = i['data_fatura']
                        faturamento_demanda.data_fatura = converter_string_para_data(data_string)
                    faturamento_demanda.save()
                    
                    self.salvar_tipo_valor_hora_faturamento(faturamento_demanda, tipovalorhoras_list)
                    
            else:
                if 'id' in i:
                    faturamento_demanda = FaturamentoDemanda.objects.get(pk=i['id'])
                    faturamento_demanda.delete()

    def salvar_tipo_valor_hora_faturamento(self, faturamento_demanda, tipovalorhoras_list):
        
        for t in tipovalorhoras_list:
            if 'remover' not in t or t['remover'] is False:
                
                tipo_valor_hora = None
                if 'tipo_hora' in t:
                    tipo_hora = t['tipo_hora']
                    if tipo_hora is not None and 'id' in tipo_hora:
                        if tipo_hora['id'] is not None:
                            tipo_valor_hora = TipoValorHora(pk=tipo_hora['id'])
                    del t['tipo_hora']
                    
                if tipo_valor_hora is not None:
                    tipo_valor_hora_faturamento = TipoValorHoraFaturamento(**t)
                    tipo_valor_hora_faturamento.faturamento_demanda = faturamento_demanda
                
                
                    tipo_valor_hora_faturamento.tipo_hora = tipo_valor_hora
                                    
                    tipo_valor_hora_faturamento.save()
                
            else:
                if 'id' in t:
                    tipo_valor_hora_faturamento = TipoValorHoraFaturamento.objects.get(pk=t['id'])
                    tipo_valor_hora_faturamento.delete()

    
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

    def post(self, request, format=None):
        
        data = request.data
        
        cliente = data['cliente']
        cliente = Cliente.objects.get(pk=cliente['id'])
        
        centro_resultado = data['centro_resultado']
        centro_resultado = CentroResultado.objects.get(pk=centro_resultado['id'])
        
        itens_faturamento = data['itens_faturamento']
        propostas = data['propostas']
        tarefas = data['tarefas']
        observacoes = data['observacoes']
        ocorrencias = data['ocorrencias']
        
        del data['cliente']
        del data['centro_resultado']
        del data['itens_faturamento']
        del data['propostas']
        del data['tarefas']
        del data['observacoes']
        del data['ocorrencias']
       
        demanda = Demanda(**data)
        demanda.cliente = cliente
        demanda.centro_resultado = centro_resultado
       
        if 'data_aprovacao_demanda' in data:
            data_string = data['data_aprovacao_demanda']
            demanda.data_aprovacao_demanda = converter_string_para_data(data_string)
            
        demanda.save();
        
        self.salvar_tarefa(tarefas, demanda)
        self.salvar_proposta(propostas, demanda)
        self.salvar_item_faturamento(itens_faturamento, demanda)
        self.salvar_observacoes(observacoes, demanda)
        self.salvar_ocorrencias(ocorrencias, demanda)
        
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