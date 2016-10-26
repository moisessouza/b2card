from django.shortcuts import render
from django.template.context_processors import request

# Create your views here.

def index(request):
    return render(request, 'clientes/index.html')