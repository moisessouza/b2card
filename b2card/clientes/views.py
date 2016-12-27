from django.shortcuts import render, redirect
from django.template.context_processors import request
from .models import Cliente
from .forms import ClienteForm
from rest_framework.views import APIView
from clientes import serializers
from rest_framework.response import Response

from datetime import datetime
from rest_framework.decorators import api_view
from cadastros.models import CentroCusto

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
        clienteSerializer = serializers.ClienteSerializer(cliente)
        
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
            
        return Response(data)
    
    def post(self, request, format=None):
                      
        data = request.data
        
        if 'dia_data_contratacao' in data:
            del data['dia_data_contratacao']
            del data['mes_data_contratacao']
            del data['ano_data_contratacao']
            
        if 'dia_data_rescisao' in data:
            del data['dia_data_rescisao']
            del data['mes_data_rescisao']
            del data['ano_data_rescisao']
        
        centro_custo = None
        if 'centro_custo' in data:
            if data['centro_custo']['id']:
                centro_custo = CentroCusto.objects.get(pk=data['centro_custo']['id'])
            del data['centro_custo']
            
        cliente = Cliente(**data)
        
        cliente.centro_custo = centro_custo
        
        data_string = request.data['data_contratacao']
        data = datetime.strptime(data_string, '%d/%m/%Y')
        cliente.data_contratacao = data.date()
        
        if 'data_rescisao' in request.data:
            data_string = request.data['data_rescisao']
            if data_string is not None:
                data = datetime.strptime(data_string, '%d/%m/%Y')
                cliente.data_rescisao = data.date()
        
        cliente.save();
        
        return self.get(request, cliente.id, format);
    
    def delete(self, request, cliente_id, format=None):
        
        cliente = Cliente.objects.get(pk=cliente_id)
        cliente.delete()
        
        serializer = serializers.ClienteSerializer(cliente)
        return Response(serializer.data)
