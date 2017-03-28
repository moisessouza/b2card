from django.shortcuts import render
from rest_framework.decorators import api_view
from mensagens.models import Mensagem
from rest_framework.response import Response
from mensagens.serializers import MensagemSerializer

# Create your views here.

@api_view(['GET'])
def list(request, format=None):
    mensagens = Mensagem.objects.filter(pessoa_fisica__prestador__usuario__id = request.user.id, lido=False)
    return Response(MensagemSerializer(mensagens, many=True).data)
    