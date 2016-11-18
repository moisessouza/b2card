from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView

from cadastros.models import ValorHora, Vigencia, CentroCusto, CentroResultado, ContaGerencial, NaturezaOperacao, \
    TipoHora
from cadastros.serializers import ValorHoraSerializer, VigenciaSerializer
from utils.utils import formatar_data, converter_string_para_float, converter_string_para_data

def index(request):
    
    valor_horas = ValorHora.objects.all()
    
    context = {
        'valor_horas': valor_horas
    }
    
    return render(request, 'valor_hora/index.html', context)

def novo(request):
    return render(request, 'valor_hora/valorhora.html')

def editar(request, valorhora_id):
    valor_hora = ValorHora.objects.get(pk=valorhora_id)
    
    context = {
        'valor_hora' : valor_hora
    }
    
    return render(request, 'valor_hora/valorhora.html', context)

class ValorHoraDetail(APIView):
    def serializar_valor_hora (self, id):
        
        valor_hora = ValorHora.objects.get(pk=id)
        data = ValorHoraSerializer(valor_hora).data;
        
        vigencias = Vigencia.objects.filter(valor_hora__id = valor_hora.id)
        
        vigencia_list = []
        
        for vigencia in vigencias:
            vigencia_data = VigenciaSerializer(vigencia).data
            vigencia_data['data_inicio'] = formatar_data(vigencia.data_inicio)
            vigencia_data['data_fim'] = formatar_data(vigencia.data_fim)
            vigencia_list.append(vigencia_data)
           
        data['vigencias'] = vigencia_list
        return Response(data)
    
    def get(self, request, valorhora_id):
        return self.serializar_valor_hora(valorhora_id);
    
    def post(self, request, format=None):
        
        data = request.data
        
        vigencia_list = None
        if 'vigencias' in data:
            vigencia_list = data['vigencias']
            del data['vigencias']
            
        centro_custo = CentroCusto.objects.get(pk=data['centro_custo']['id'])
        del data['centro_custo']
        
        centro_resultado = CentroResultado.objects.get(pk=data['centro_resultado']['id'])
        del data['centro_resultado']
        
        conta_gerencial = ContaGerencial.objects.get(pk=data['conta_gerencial']['id'])
        del data['conta_gerencial']
        
        natureza_operacao = NaturezaOperacao.objects.get(pk=data['natureza_operacao']['id'])
        del data['natureza_operacao']
        
        tipo_hora = TipoHora.objects.get(pk=data['tipo_hora']['id'])
        del data['tipo_hora']
        
        valor_hora = ValorHora(**data)
        valor_hora.centro_custo = centro_custo
        valor_hora.centro_resultado = centro_resultado
        valor_hora.conta_gerencial = conta_gerencial
        valor_hora.natureza_operacao = natureza_operacao
        valor_hora.tipo_hora = tipo_hora
        
        valor_hora.save()
        
        for vigencia in vigencia_list:
            
            if 'data_inicio' in vigencia and 'data_fim' in vigencia and 'valor' in vigencia:
                data_inicio = converter_string_para_data(vigencia['data_inicio'])
                data_fim = converter_string_para_data(vigencia['data_fim'])
                valor = converter_string_para_float(vigencia['valor'])
                
                id = None
                if 'id' in vigencia:
                    id = vigencia['id']
                    
                v = Vigencia(data_inicio=data_inicio, 
                             data_fim=data_fim, 
                             valor=valor, 
                             id=id,
                             valor_hora=valor_hora)
                v.save()
            
        
        return self.serializar_valor_hora(valor_hora.id)
    
    def delete(self, request, valorhora_id):
        
        valor_hora = ValorHora.objects.get(pk=valorhora_id)
        valor_hora.delete()
               
        return Response('ok')