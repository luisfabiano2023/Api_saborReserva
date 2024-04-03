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
        'Minha API': 'minha/api',
        'Criar Vendedor': 'criar/vendedor',
        'Criar Lanche': 'criar/lanche',
        'Listar Vendedores': 'listar/vendedores',
        'Listar Lanches': 'listar/lanches',
        'Listar Vendedor': 'listar/vendedor/<int:pk>',
        'Listar Lanche': 'listar/lanche/<int:pk>',
        'Atualizar Vendedor': 'atualizar/vendedor/<int:pk>',
        'Atualizar Lanche': 'atualizar/lanche/<int:pk>',
        'Excluir Vendedor': 'excluir/vendedor/<int:pk>',
        'Excluir Lanche': 'excluir/lanche/<int:pk>'
     }

     return Response(api_urls)


class MinhaAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        content = {'message': 'Deu tudo certo rapaziada!!!!'}
        return Response(content)
    

@api_view(['POST'])
def criar_vendedor(request):
    try:
        vendedor_v = vendedorSerializer(data=request.data)

        if Vendedor.objects.filter(**request.data).exists():
            raise serializers.ValidationError('Esse vendedor ja foi cadastrado')

        if vendedor_v.is_valid():
            vendedor_v.save()
            return Response({"message": "Vendedor criado com sucesso", "data": vendedor_v.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({"message": "Dados inválidos para criar vendedor"}, status=status.HTTP_400_BAD_REQUEST)
    except Vendedor.DoesNotExist:
        return Response({"message": "Vendedor não encontrado"}, status=status.HTTP_404_NOT_FOUND)
 

@api_view(['POST'])
def criar_lanche(request):
    try:
        lanche_l = lancheSerializer(data=request.data)

        if Lanche.objects.filter(**request.data).exists():
            raise serializers.ValidationError('Este lanche já foi cadastrado')

        if lanche_l.is_valid():
            lanche_l.save()
            return Response({"message": "Lanche criado com sucesso", "data": lanche_l.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({"message": "Dados inválidos para criar lanche"}, status=status.HTTP_400_BAD_REQUEST)
    except Lanche.DoesNotExist:
        return Response({"message": "Lanche não encontrado"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def listar_vendedores(request):
     try:
          vendedores = Vendedor.objects.all()
          serializer = vendedorSerializer(vendedores, many=True)
          return Response(serializer.data)
     except Vendedor.DoesNotExist:
          return Response({"message": "Não há vendedores registrados."}, status=status.HTTP_404_NOT_FOUND)
     

@api_view(['GET'])
def listar_lanches(request):
     try: 
          lanches = Lanche.objects.all()
          serializer = lancheSerializer(lanches, many=True)
          return Response(serializer.data)
     except Lanche.DoesNotExist:
          return Response({"message": "Não há lanches registrados."}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def listar_vendedor(request, pk):
    try:
        vendedor = Vendedor.objects.get(pk=pk)
        serializer = vendedorSerializer(instance=vendedor)
        return Response(serializer.data)
    except Vendedor.DoesNotExist:
        return Response({"message": "O vendedor com o ID fornecido não foi encontrado."}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def listar_lanche(request, pk):
    try:
        lanche = Lanche.objects.get(pk=pk)
        serializer = lancheSerializer(instance=lanche)
        return Response(serializer.data)
    except Lanche.DoesNotExist:
        return Response({"message": "O lanche com o ID fornecido não foi encontrado."}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def  atualizar_vendedor(request, pk):
     try:
        vendedor = Vendedor.objects.get(pk=pk)
        serializer = vendedorSerializer(instance=vendedor, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Vendedor atualizado com sucesso", "data": serializer.data})
        else:
            return Response({"message": "Dados inválidos para atualizar vendedor"}, status=status.HTTP_400_BAD_REQUEST)
     except Vendedor.DoesNotExist:
        return Response({"message": "Vendedor não encontrado"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def atualizar_lanche(request,pk):
     try:
        lanche = Lanche.objects.get(pk=pk)
        serializer = lancheSerializer(instance=lanche, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Lanche atualizado com sucesso", "data": serializer.data})
        else:
            return Response({"message": "Dados inválidos para atualizar lanche"}, status=status.HTTP_400_BAD_REQUEST)
     except Lanche.DoesNotExist:
        return Response({"message": "Lanche não encontrado"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['DELETE'])
def excluir_vendedor(request, pk):
    try:
        vendedor = Vendedor.objects.get(pk=pk)
        vendedor.delete()
        return Response({"message": "Vendedor excluído com sucesso."}, status=status.HTTP_204_NO_CONTENT)
    except Vendedor.DoesNotExist:
        return Response({"message": "O vendedor com o ID fornecido não foi encontrado."}, status=status.HTTP_404_NOT_FOUND)


@api_view(['DELETE'])
def excluir_lanche(request, pk):
    try:
        lanche = Lanche.objects.get(pk=pk)
        lanche.delete()
        return Response({"message": "Lanche excluído com sucesso."}, status=status.HTTP_204_NO_CONTENT)
    except Lanche.DoesNotExist:
        return Response({"message": "O lanche com o ID fornecido não foi encontrado."}, status=status.HTTP_404_NOT_FOUND)
    


