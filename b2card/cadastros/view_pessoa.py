from django.shortcuts import render
from cadastros.models import TipoHora, CentroCusto
from cadastros import serializers
from rest_framework.response import Response
from rest_framework.views import APIView

def index(request):
    return render(request, 'pessoa/index.html')

def novo(request):
    return render(request, 'pessoa/cadastro.html')