from django.shortcuts import render, redirect
from django.template.context_processors import request
from .models import Cliente
from .forms import ClienteForm
from rest_framework.views import APIView
from clientes import serializers
from rest_framework.response import Response
from clientes.models import TipoValorHora, CentroResultado
from datetime import datetime
from rest_framework.decorators import api_view

# Create your views here.

def index(request):
    clientes = Cliente.objects.all()
    
    context = {
        'clientes': clientes
    }   
    
    return render(request, 'clientes/index.html', context)

def novo(request):
    return render(request, 'clientes/cliente.html')

def editar(request, cliente_id):
    
    cliente = Cliente.objects.get(pk=cliente_id)
    
    context = {
        'cliente': cliente
    }

    return render(request, 'clientes/cliente.html', context) 
''' 
    API REST
''' 
class ClienteList(APIView):
    def get(self, request, format=None):
        clientes = Cliente.objects.all()
        serializer = serializers.ClienteMinSerializer(clientes, many=True)
        return Response(serializer.data)
    
class ClienteDetail(APIView):
    def get(self, request, cliente_id, format=None):
        
        cliente = Cliente.objects.get(pk=cliente_id)
        tipos_valor_hora = TipoValorHora.objects.filter(cliente=cliente)
        clienteSerializer = serializers.ClienteSerializer(cliente)
        centro_resultados = CentroResultado.objects.filter(cliente=cliente)
        
        data = clienteSerializer.data
        
        iso = cliente.data_contratacao.isoformat()
        tokens = iso.strip()
        tokens = iso.split('-')
        data['data_contratacao'] = "%s/%s/%s" % (tokens[2],tokens[1],tokens[0])
        
        if cliente.data_rescisao is not None:
            iso = cliente.data_contratacao.isoformat()
            tokens = iso.strip()
            tokens = iso.split('-')
            data['data_rescisao'] = "%s/%s/%s" % (tokens[2],tokens[1],tokens[0])
            
        tipos_valor_hora = serializers.TipoValorHoraSerializer(tipos_valor_hora, many=True)
        data['tipovalorhora'] = tipos_valor_hora.data
        
        centro_resultados = serializers.CentroResultadoSerializer(centro_resultados, many=True)
        data['centroresultados'] = centro_resultados.data
        
        return Response(data)
    
    def post(self, request, format=None):
                      
        data = request.data
        
        if 'tipovalorhora' in request.data:
            tipos_valor_hora = data['tipovalorhora']
            del data['tipovalorhora']
            
        if 'centroresultados' in data:
            centro_resultados = data['centroresultados']
            del data['centroresultados']
        
        if 'dia_data_contratacao' in data:
            del data['dia_data_contratacao']
            del data['mes_data_contratacao']
            del data['ano_data_contratacao']
            
        if 'dia_data_rescisao' in data:
            del data['dia_data_rescisao']
            del data['mes_data_rescisao']
            del data['ano_data_rescisao']
        
        cliente = Cliente(**data)
        
        data_string = request.data['data_contratacao']
        #data_string = data_string[:data_string.index('T')]
        data = datetime.strptime(data_string, '%d/%m/%Y')
        cliente.data_contratacao = data.date()
        
        if 'data_rescisao' in request.data:
            data_string = request.data['data_rescisao']
            if data_string is not None:
                #data_string = data_string[:data_string.index('T')]
                data = datetime.strptime(data_string, '%d/%m/%Y')
                cliente.data_rescisao = data.date()
        
        cliente.save();
        
        if tipos_valor_hora is not None:
            for tipo_valor_hora in tipos_valor_hora:
                if (tipo_valor_hora['tipo_hora'] is not None 
                    and tipo_valor_hora['valor_hora'] is not None):
                    tipo_valor = TipoValorHora(**tipo_valor_hora)
                    tipo_valor.cliente = cliente
                    tipo_valor.save()
                    
        if centro_resultados is not None:
            for centro_resultado in centro_resultados:
                if centro_resultado['razao_social'] is not None and centro_resultado['cnpj'] is not None:
                    centro_result = CentroResultado(**centro_resultado)
                    centro_result.cliente = cliente
                    centro_result.save()
                
        return self.get(request, cliente.id, format);
    
    def delete(self, request, cliente_id, format=None):
        
        cliente = Cliente.objects.get(pk=cliente_id)
        
        tipos_valor_hora = TipoValorHora.objects.filter(cliente=cliente)
        
        for tipo_valor_hora in tipos_valor_hora:
            tipo_valor_hora.delete()
            
        cliente.delete()
        
        serializer = serializers.ClienteSerializer(cliente)
        return Response(serializer.data)
    
class TipoValorHoraDetail(APIView):
    
    def get(self, request, tipo_valor_hora_id, format=None):
        tipo_valor_hora  = TipoValorHora.objects.get(pk=tipo_valor_hora_id)
        serializer = serializers.TipoValorHoraSerializer(tipo_valor_hora)
        return Response(serializer.data)
    
    def delete(self, request, tipo_valor_hora_id, format=None):
        
        tipo_valor_hora = TipoValorHora.objects.get(pk=tipo_valor_hora_id)
        tipo_valor_hora.delete()
        
        serializer = serializers.TipoValorHoraSerializer(tipo_valor_hora)
        return Response(serializer.data)

class CentroResultadoDetail(APIView):
    
    def delete(self, request, centro_resultado_id, format=None):
        centro_resultado = CentroResultado.objects.get(pk=centro_resultado_id)
        centro_resultado.delete()
        
        serializer = serializers.CentroResultadoSerializer(centro_resultado)
        return Response(serializer.data)
    
@api_view(['GET', 'PUT', 'DELETE'])
def buscar_valor_hora_cliente(request, cliente_id):
    
    tipo_valor_horas = TipoValorHora.objects.filter(cliente__id=cliente_id)
    serializer = serializers.TipoValorHoraSerializer(tipo_valor_horas, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def buscar_centro_resultados_cliente(request, cliente_id):
    centro_resultados = CentroResultado.objects.filter(cliente__id = cliente_id)
    serializer = serializers.CentroResultadoSerializer(centro_resultados, many=True)
    return Response(serializer.data)
