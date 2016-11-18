from django.shortcuts import render

def index(request):
    return render(request, 'tipo_hora/index.html');