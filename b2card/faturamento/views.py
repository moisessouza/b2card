from django.shortcuts import render
from rest_framework.views import APIView
from faturamento.models import Parcela
from faturamento.serializers import ParcelaSerializer
from rest_framework.response import Response
from utils.utils import converter_string_para_float, converter_string_para_data
from demandas.models import Demanda

# Create your views here.

class ParcelaList(APIView):
    
    def post(self, request, format=None):
        
        parcelas = []
        
        for i in request.data:
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
                
                parcelas.append(parcela)
                
            elif 'id' in i:
                parcela = Parcela.objects.get(pk=i['id'])
                parcela.delete()
                
        serializer = ParcelaSerializer(parcelas, many=True)
        
        return Response(serializer.data)