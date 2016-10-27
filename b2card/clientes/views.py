from django.shortcuts import render, redirect
from django.template.context_processors import request
from .models import Cliente
from .forms import ClienteForm
from rest_framework.views import APIView
from clientes import serializers
from rest_framework.response import Response

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
    
def executar(request):
    
    if 'gravar' in request.POST:
    
        if 'id' in request.POST and request.POST['id']:
            cliente = Cliente.objects.get(pk=request.POST['id'])
            form = ClienteForm(request.POST, instance=cliente)
        else:
            form = ClienteForm(request.POST)
        form.save()
        
        context = {
            'success':{
                'message': 'Cliente gravado com sucesso!'
            }
        }
        return render(request, 'clientes/cliente.html', context)
    
    elif 'deletar' in request.POST:
        cliente = Cliente.objects.get(pk=request.POST['id'])
        cliente.delete()
        return redirect('clientes:inicial')
    

''' 
    API REST
''' 
class ClienteList(APIView):
    def get(self, request, format=None):
        materiais = Cliente.objects.all()
        serializer = serializers.ClienteSerializer(materiais, many=True)
        return Response(serializer.data)