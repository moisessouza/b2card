from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from demandas.models import Demanda, FaturamentoDemanda
from datetime import datetime
from demandas import serializers
from clientes.models import Cliente, TipoValorHora
from demandas.serializers import DemandaSerializer, FaturamentoDemandaSerializer
import demandas

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
        
        demanda = Demanda.objects.get(pk=demanda_id)
        itens_faturamento = FaturamentoDemanda.objects.filter(demanda__id = demanda_id)
        
        data = DemandaSerializer(demanda).data
        
        itens = []
        
        for i in itens_faturamento:
            faturamento_demanda = FaturamentoDemandaSerializer(i).data
            faturamento_demanda['data'] = formatar_data(i.data)
            faturamento_demanda['data_envio_aprovacao'] = formatar_data(i.data_envio_aprovacao)
            faturamento_demanda['data_aprovacao_fatura'] = formatar_data(i.data_aprovacao_fatura)
            faturamento_demanda['data_fatura'] = formatar_data(i.data_fatura)
            itens.append(faturamento_demanda)
            
        data['itens_faturamento'] = itens
        
        return Response(data)
    
    def post(self, request, format=None):
        
        data = request.data
        
        cliente = data['cliente']
        cliente = Cliente.objects.get(pk=cliente['id'])
        
        itens_faturamento = data['itens_faturamento']
        
        del data['cliente']
        del data['itens_faturamento']
       
        demanda = Demanda(**data)
        demanda.cliente = cliente
        
        demanda.save();
        
        for i in itens_faturamento:
            
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
                data = datetime.strptime(data_string, '%d/%m/%Y')
                faturamento_demanda.data = data.date()
            if 'data_envio_aprovacao' in i:
                data_string = i['data_envio_aprovacao']
                data = datetime.strptime(data_string, '%d/%m/%Y')
                faturamento_demanda.data_envio_aprovacao = data.date()
            if 'data_aprovacao_fatura' in i:
                data_string = i['data_aprovacao_fatura']
                data = datetime.strptime(data_string, '%d/%m/%Y')
                faturamento_demanda.data_aprovacao_fatura = data.date()
            if 'data_fatura' in i:
                data_string = i['data_fatura']
                data = datetime.strptime(data_string, '%d/%m/%Y')
                faturamento_demanda.data_fatura = data.date()
            
            faturamento_demanda.save()
            
        serializer = serializers.DemandaSerializer(demanda)
        
        return Response(serializer.data)
    
    def delete(self, request, demanda_id, format=None):
        
        demanda = Demanda.objects.get(pk=demanda_id)
        faturamento_demanda =  FaturamentoDemanda.objects.filter(demanda=demanda)
        
        for i in faturamento_demanda:
            i.delete()
            
        demanda.delete()
        
        data = DemandaSerializer(demanda).data
        data['data_aprovacao'] = formatar_data(demanda.data_aprovacao)
        
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
        

def formatar_data(data):
    if data is not None:
        iso = data.isoformat()
        tokens = iso.strip()
        tokens = iso.split('-')
        return "%s/%s/%s" % (tokens[2],tokens[1],tokens[0])
    else:
        return None
    