from urllib import request
from django.shortcuts import render
from rest_framework import serializers
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Vendedor,Lanche
from .serializers import vendedorSerializer,lancheSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView



@api_view(['GET'])
def api_geral(request):
     api_urls = {
        'all_vendedores': '/',
        'all_lanches': '/',
        'read_vendedor': '/read/pk',
        'read_lanche': '/read/pk',
        'Add': '/create',
        'Update': '/update/pk',
        'Delete': '/item/pk/delete'
     }

     return Response(api_urls)


@api_view(['GET'])
def listar_vendedores(request):
     try:
          vendedores = Vendedor.objects.all()
          serializer = vendedorSerializer(vendedores, many=True)
          return Response(serializer.data)
     except Vendedor.DoesNotExist:
          return Response(status=status.HTTP_404_NOT_FOUND)
     

@api_view(['GET'])
def listar_lanches(request):
     try: 
          lanches = Lanche.objects.all()
          serializer = lancheSerializer(lanches, many=True)
          return Response(serializer.data)
     except Lanche.DoesNotExist:
          return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def listar_vendedor(request, pk):
    try:
        vendedor = Vendedor.objects.get(pk=pk)
        serializer = vendedorSerializer(instance=vendedor)
        return Response(serializer.data)
    except Vendedor.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def listar_lanche(request, pk):
    try:
        lanche = Lanche.objects.get(pk=pk)
        serializer = lancheSerializer(instance=lanche)
        return Response(serializer.data)
    except Lanche.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
     

@api_view(['POST'])
def criar_vendedor(request):
    vendedor_v = vendedorSerializer(data=request.data)
 
    # validating for already existing data
    if Vendedor.objects.filter(**request.data).exists():
        raise serializers.ValidationError('This data already exists')
 
    if vendedor_v.is_valid():
        vendedor_v.save()
        return Response(vendedor_v.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def criar_lanche(request):
    lanche_l = lancheSerializer(data=request.data)
 
    # validating for already existing data
    if Lanche.objects.filter(**request.data).exists():
        raise serializers.ValidationError('Esse lanche já foi cadastrado')
 
    if lanche_l.is_valid():
        lanche_l.save()
        return Response(lanche_l.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def  atualizar_vendedor(request, pk):
     vendedor = vendedor.objects.get(pk=pk)
     data = vendedorSerializer(instance=vendedor, data=request.data)
     
     if data.is_valid():
         data.save()
        return Response(data.data)
     else:
        return Response(status=status.HTTP_404_NOT_FOUND)
          
def atualizar_lanche(request,pk):
     lanche = lanche.objects.get(pk=pk)
     data = lancheSerializer(instance=lanche, data=request.data)
 
     if data.is_valid():
         data.save()
        return Response(data.data)
     else:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
class MinhaAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        content = {'message': 'Deu tudo certo rapaziada!!!!'}
        return Response(content)
