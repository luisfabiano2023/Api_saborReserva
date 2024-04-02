from urllib import request
from django.shortcuts import render
from rest_framework import serializers
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Vendedor,Lanche
from .serializers import vendedorSerializer,lancheSerializer


@api_view(['GET'])
def api_geral(request):
     api_urls = {
        'all_vendedores': '/',
        'Search by Vendedor': '/?nome_vendedor=nome_vendedor_name',
        'all_lanches': '/',
        'Search by Produto': '/?produto_oferecido=produto_oferecido_name',
        'Add': '/create',
        'Update': '/update/pk',
        'Delete': '/item/pk/delete'
     }

     return Response(api_urls)


@api_view(['GET'])
def listar_vendedores(request):
     
     if request.query_params:
          vendedores = Vendedor.objects.filter(**request.query_params.dict())
     else:
          vendedores = Vendedor.objects.all()

     if vendedores:
          serializer = vendedorSerializer(vendedores, many=True)
          return Response(serializer.data)
     else:
          return Response(status=status.HTTP_404_NOT_FOUND)
     

@api_view(['GET'])
def listar_lanches(request):
     
     if request.query_params:
          lanches = Lanche.objects.filter(**request.query_params.dict())
     else:
          lanches = Lanche.objects.all()

     if lanches:
          serializer = lancheSerializer(lanches, many=True)
          return Response(serializer.data)
     else:
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
