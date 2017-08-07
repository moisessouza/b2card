from django.shortcuts import render
from django.db.models import Q
from rest_framework.response import Response
from rest_framework.views import APIView

from cadastros.models import ValorHora, Vigencia, CentroCusto, CentroResultado, ContaGerencial, NaturezaOperacao, \
    TipoHora
from cadastros.serializers import ValorHoraSerializer, VigenciaSerializer
from utils.utils import formatar_data, converter_string_para_float, converter_string_para_data,\
    formatar_para_valor_monetario, converter_data_url
from rest_framework.decorators import api_view
import datetime

def index(request):
    
    valor_horas = ValorHora.objects.all().order_by('centro_custo__nome','tipo_hora__descricao', 'descricao')
    
    for i in valor_horas:
        vigencia = Vigencia.objects.filter(valor_hora=i, data_inicio__lte = datetime.date.today(), data_fim__gte = datetime.date.today())
        if vigencia:
            i.vigencia = vigencia[0]
            i.vigencia.valor = formatar_para_valor_monetario(i.vigencia.valor)
    
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
    
@api_view(['GET'])
def buscar_valor_hora_por_cliente(request, cliente_id, data, format=None):
    
    data = converter_data_url(data)
    
    valor_horas = ValorHora.objects.filter(Q(centro_custo__apropriacao__pessoa__pessoajuridica__id = cliente_id) & Q(tipo_hora__descricao = 'Valor de Venda para Clientes'));
    
    valor_hora_list = []
    for i in valor_horas:
        vigencia = Vigencia.objects.filter(valor_hora=i, data_inicio__lte = data).filter(Q(data_fim__isnull=True) | Q(data_fim__gte = data))
        if vigencia:
            valor_hora_data = ValorHoraSerializer(i).data    
            valor_hora_data['vigencia'] = VigenciaSerializer(vigencia[0]).data
            valor_hora_list.append(valor_hora_data)

    return Response(valor_hora_list)

@api_view(['GET'])
def buscar_valor_lucro_risco_por_cliente(request, cliente_id, data, format=None):
    
    data = converter_data_url(data)
    
    valor_horas = ValorHora.objects.filter(Q(centro_custo__apropriacao__pessoa__pessoajuridica__id = cliente_id) & Q(centro_resultado__nome = 'B2Card'));
    
    valor_hora_list = []
    for i in valor_horas:
        vigencia = Vigencia.objects.filter(valor_hora=i, data_inicio__lte = data).filter(Q(data_fim__isnull=True) | Q(data_fim__gte = data))
        if vigencia:
            valor_hora_data = ValorHoraSerializer(i).data    
            valor_hora_data['vigencia'] = VigenciaSerializer(vigencia[0]).data
            valor_hora_list.append(valor_hora_data)

    return Response(valor_hora_list)

@api_view(['GET'])
def buscar_valor_hora_b2card(request, data, format=None):
    valor_horas = ValorHora.objects.filter(Q(centro_custo__nome='B2Card') & Q(tipo_hora__descricao='Custo Medio Interno'))
   # valor_horas = ValorHora.objects.filter(Q(centro_custo__nome='B2Card'))

    
    data = converter_data_url(data)
        
    valor_hora_list = []
    for i in valor_horas:
        vigencia = Vigencia.objects.filter(valor_hora=i, data_inicio__lte = data).filter(Q(data_fim__isnull=True) | Q(data_fim__gte = data))
        if vigencia:
            valor_hora_data = ValorHoraSerializer(i).data    
            valor_hora_data['vigencia'] = VigenciaSerializer(vigencia[0]).data
            valor_hora_list.append(valor_hora_data)
    
    return Response(valor_hora_list)    

# api para buscar custo administrativo e impostos - Nilson
@api_view(['GET'])
def buscar_valor_imposto_custoadmin_b2card(request, data, format=None):
    valor_imposto_custoadmin = ValorHora.objects.filter(Q(centro_custo__nome='B2Card') & (Q(descricao='Valor % Custo Administrativo') | Q(descricao='Valor % Impostos')))
    
    data = converter_data_url(data)
       
    #valor_taxa_total = 0
    valor_taxa_total = []
    for i in valor_imposto_custoadmin:
        vigencia = Vigencia.objects.filter(valor_hora=i, data_inicio__lte = data).filter(Q(data_fim__isnull=True) | Q(data_fim__gte = data))
        if vigencia:
            valor_taxa_data = ValorHoraSerializer(i).data    
            valor_taxa_data['vigencia'] = VigenciaSerializer(vigencia[0]).data
            valor_taxa_total.append(valor_taxa_data)
    
    return Response(valor_taxa_total)   


@api_view(['GET'])
def buscar_valor_horas(request):
    
    valor_horas = ValorHora.objects.all(); 
    
    valor_hora_list = []
    for i in valor_horas:
        vigencia = Vigencia.objects.filter(valor_hora=i, data_inicio__lte = datetime.date.today(), data_fim__gte = datetime.date.today())
        if vigencia:
            valor_hora_data = ValorHoraSerializer(i).data    
            valor_hora_data['vigencia'] = VigenciaSerializer(vigencia[0]).data
            valor_hora_list.append(valor_hora_data)

    return Response(valor_hora_list)
    
