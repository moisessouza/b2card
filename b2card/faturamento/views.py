from django.shortcuts import render
from rest_framework.views import APIView
from faturamento.models import Parcela, Medicao, ParcelaFase
from faturamento.serializers import ParcelaSerializer, MedicaoSerializer, ParcelaFaseSerializer
from rest_framework.response import Response
from utils.utils import converter_string_para_float, converter_string_para_data, formatar_data
from demandas.models import Demanda, Fase
from exceptions import Exception
from cadastros.models import ValorHora, TipoHora, Vigencia
from rest_framework.decorators import api_view
from demandas.serializers import FaseSerializer
from cadastros.serializers import TipoHoraSerializer, ValorHoraSerializer, VigenciaSerializer
import datetime

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
                
                parcelafase_list = []
                if 'parcelafases' in i:
                    parcelafase_list = i['parcelafases']
                    del i['parcelafases']
                
                parcela = Parcela(**i)
                parcela.valor_parcela = valor_parcela
                parcela.data_previsto_parcela = data_previsto_parcela
                parcela.tipo_parcela = tipo_parcela
                parcela.demanda = demanda
                parcela.save()
                
                parcelafase_resp = self.gravar_parcelafases(parcela, parcelafase_list)

                serializer = ParcelaSerializer(parcela).data
                serializer['data_previsto_parcela'] = formatar_data(parcela.data_previsto_parcela)
                serializer['parcelafases'] = parcelafase_resp
                parcela_resp.append(serializer)
                
            elif 'id' in i:
                parcela = Parcela.objects.get(pk=i['id'])
                parcela.delete()
        
        context = {
            'tipo_parcela': tipo_parcela,
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
                        fase = Fase.objects.get(pk=i['fase']['id'])
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
                    medicao.valor = converter_string_para_float(medicao.valor)   
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
    
    fase_list = Fase.objects.filter(orcamento__demanda__id=demanda_id)
    
    faseserializer_list = []
    
    for i in fase_list:
        serializer = FaseSerializer(i).data
        faseserializer_list.append(serializer)
        valor_horas = ValorHora.objects.filter(itemfase__fase = i).distinct()
        
        valor_hora_list = []
        for i in valor_horas:
            vigencia = Vigencia.objects.filter(valor_hora=i, data_inicio__lte = datetime.date.today(), data_fim__gte = datetime.date.today())
            if vigencia:
                valor_hora_data = ValorHoraSerializer(i).data    
                valor_hora_data['vigencia'] = VigenciaSerializer(vigencia[0]).data
                valor_hora_list.append(valor_hora_data)
        
        serializer['valorhora'] = valor_hora_list
        
    
    return Response(faseserializer_list)
    
    