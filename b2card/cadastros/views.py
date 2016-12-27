from django.shortcuts import render
from rest_framework.views import APIView

# Create your views here.
def index(request):
    return render(request, 'template/index.html');

