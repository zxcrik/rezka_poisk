from django.shortcuts import render
from rest_framework.views import APIView     
from rest_framework.response import Response 
from .models import *
from .serializers import *


# Create your views here.

class FilmApiView(APIView):           
    def get(self,request):
        return Response({'title':'Побег из шоушенка'})
    
    def post(self, request):
        print(request.data)
        return Response({'title':'The shawshank Redemption'})
    

# get - получить инф #
# post - передать данные #
# delete - удалить данные #
# put - Изменить данные #
# Patch - изменение нескольких данных #