from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, 'demandas/index.html')
    
def novo(request):
    return render(request, 'demandas/demanda.html')