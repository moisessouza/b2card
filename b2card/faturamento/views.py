from django.shortcuts import render
from rest_framework.views import APIView
from faturamento.models import Parcela, Medicao
from faturamento.serializers import ParcelaSerializer
from rest_framework.response import Response
from utils.utils import converter_string_para_float, converter_string_para_data, formatar_data
from demandas.models import Demanda
from exceptions import Exception
from cadastros.models import ValorHora

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
            
        tipo_parcela = None
        if 'tipo_parcela' in request.data:
            tipo_parcela = request.data['tipo_parcela']
            demanda.tipo_parcela = tipo_parcela
            demanda.save()
        
        parcela_resp = []
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
                
                demanda = None
                if 'demanda' in i:
                    demanda = Demanda.objects.get(pk=i['demanda']['id'])
                    del i['demanda']
                    
                parcela = Parcela(**i)
                parcela.valor_parcela = valor_parcela
                parcela.data_previsto_parcela = data_previsto_parcela
                parcela.demanda = demanda
                parcela.save()
                
                if tipo_parcela == 'M':
                    self.gravar_medicoes(parcela, i['medicoes'])
                
                serializer = ParcelaSerializer(parcela).data
                serializer['data_previsto_parcela'] = formatar_data(parcela.data_previsto_parcela)
                parcela_resp.append(serializer)
                
            elif 'id' in i:
                parcela = Parcela.objects.get(pk=i['id'])
                parcela.delete()
        
        return Response(parcela_resp)
    
    def gravar_medicoes(self, parcela, medicoes):
        
        medicao_list = []
        if medicoes:
            for i in medicoes:
                if 'remover' not in i or i['remover'] == False:
                    
                    valor_hora = None
                    if 'valor_hora' in i:
                        valor_hora = ValorHora.objects.get(pk=i['valor_hora']['id'])
                        del i['valor_hora']
                    
                    medicao = Medicao(**i)
                    medicao.valor = converter_string_para_float(medicao.valor)   
                    medicao.valor_total = converter_string_para_float(medicao.valor_total)
                    medicao.parcela = parcela
                    medicao.save()
                    
                    
                    
                    
                elif 'id' in i:
                    medicao = Medicao.objects.get(pk=i['id'])
                    medicao.delete()
            
            
         
        return medicao_list   