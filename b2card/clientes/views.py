from django.shortcuts import render
from django.template.context_processors import request
from .models import Cliente
from .forms import ClienteForm

# Create your views here.

def index(request):
    clientes = Cliente.objects.all()
    
    context = {
        'clientes': clientes
    }   
    
    return render(request, 'clientes/index.html', context)

def novo(request):
    return render(request, 'clientes/cliente.html')

def gravar(request):
    
    form = ClienteForm(request.POST)
    form.save()
    
    context = {
        'success':{
            'message': 'Cliente gravado com sucesso!'
        }
    }
    return render(request, 'clientes/cliente.html', context)