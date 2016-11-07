from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from demandas.models import Demanda, FaturamentoDemanda, Proposta
from demandas import serializers
from clientes.models import Cliente, TipoValorHora
from demandas.serializers import DemandaSerializer, FaturamentoDemandaSerializer, PropostaSerializer
from utils.utils import converter_string_para_data, formatar_data

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
        data = DemandaSerializer(demanda).data
        itens = []
        for i in itens_faturamento:
            faturamento_demanda = FaturamentoDemandaSerializer(i).data
            faturamento_demanda['data'] = formatar_data(i.data)
            faturamento_demanda['data_envio_aprovacao'] = formatar_data(i.data_envio_aprovacao)
            faturamento_demanda['data_aprovacao_fatura'] = formatar_data(i.data_aprovacao_fatura)
            faturamento_demanda['data_fatura'] = formatar_data(i.data_fatura)
            itens.append(faturamento_demanda)
        
        propostas_list = []
        for i in propostas:
            proposta = PropostaSerializer(i).data
            proposta['data_recimento_solicitacao'] = formatar_data(i.data_recimento_solicitacao)
            proposta['data_limite_entrega'] = formatar_data(i.data_limite_entrega)
            proposta['data_real_entrega'] = formatar_data(i.data_real_entrega)
            proposta['data_aprovacao'] = formatar_data(i.data_aprovacao)
            propostas_list.append(proposta)
        
        data['itens_faturamento'] = itens
        data['propostas'] = propostas_list
        return data

    def get(self, request, demanda_id, format=None):
        
        data = self.serializarDemanda(demanda_id)
        
        return Response(data)
    
    def post(self, request, format=None):
        
        data = request.data
        
        cliente = data['cliente']
        cliente = Cliente.objects.get(pk=cliente['id'])
        
        itens_faturamento = data['itens_faturamento']
        
        propostas = data['propostas']
        
        del data['cliente']
        del data['itens_faturamento']
        del data['propostas']
       
        demanda = Demanda(**data)
        demanda.cliente = cliente
        
        demanda.save();
        
        for i in propostas:
           
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
        
        for i in itens_faturamento:
            
            if 'descricao' in i and i['descricao'] is not None:
            
                tipo_valor_hora = None
                
                if 'tipo_hora' in i:
                    tipo_valor_hora = i['tipo_hora']
                    tipo_valor_hora = TipoValorHora(pk=tipo_valor_hora['id'])
                
                    del i['tipo_hora']
                
                faturamento_demanda = FaturamentoDemanda(**i)
                faturamento_demanda.demanda = demanda
                
                if tipo_valor_hora is not None:
                    faturamento_demanda.tipo_hora = tipo_valor_hora
               
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