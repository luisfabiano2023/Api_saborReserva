from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Vendedor, Produto, Cliente
from .serializers import VendedorSerializer, ProdutoSerializer, ClienteSerializer
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.tokens import AccessToken


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_geral(request):
    user = request.user
    access_token = AccessToken.for_user(user)
    
    api_urls = {
        'Minha API': 'minha/api',
        'Criar Vendedor': 'criar/vendedor',
        'Criar Produto': 'criar/produto',
        'Listar Vendedores': 'listar/vendedores',
        'Listar Produtos': 'listar/produtos',
        'Listar Vendedor': 'listar/vendedor/<int:pk>',
        'Listar Produto': 'listar/produto/<int:pk>',
        'Atualizar Vendedor': 'atualizar/vendedor/<int:pk>',
        'Atualizar Produto': 'atualizar/produto/<int:pk>',
        'Excluir Vendedor': 'excluir/vendedor/<int:pk>',
        'Excluir produto': 'excluir/produto/<int:pk>',
        'Access Token': str(access_token),
    }
    return Response(api_urls)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def minha_api_view(request):
    content = {'message': 'Deu tudo certo rapaziada!!!!'}
    return Response(content)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def criar_vendedor(request):
    serializer = VendedorSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Vendedor criado com sucesso", "data": serializer.data}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def criar_produto(request):
    serializer = ProdutoSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Produto criado com sucesso", "data": serializer.data}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def listar_vendedores(request):
    vendedores = Vendedor.objects.all()
    serializer = VendedorSerializer(vendedores, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def listar_produtos(request):
    produtos = Produto.objects.all()
    serializer = ProdutoSerializer(produtos, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def listar_vendedor(request, pk):
    try:
        vendedor = Vendedor.objects.get(pk=pk)
    except Vendedor.DoesNotExist:
        return Response({"message": "O vendedor com o ID fornecido não foi encontrado."}, status=status.HTTP_404_NOT_FOUND)
    serializer = VendedorSerializer(vendedor)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def listar_produto(request, pk):
    try:
        produto = Produto.objects.get(pk=pk)
    except produto.DoesNotExist:
        return Response({"message": "O produto com o ID fornecido não foi encontrado."}, status=status.HTTP_404_NOT_FOUND)
    serializer = ProdutoSerializer(produto)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def atualizar_vendedor(request, pk):
    try:
        vendedor = Vendedor.objects.get(pk=pk)
    except Vendedor.DoesNotExist:
        return Response({"message": "Vendedor não encontrado"}, status=status.HTTP_404_NOT_FOUND)
    serializer = VendedorSerializer(instance=vendedor, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Vendedor atualizado com sucesso", "data": serializer.data})
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def atualizar_produto(request,pk):
    try:
        produto = Produto.objects.get(pk=pk)
    except Produto.DoesNotExist:
        return Response({"message": "produto não encontrado"}, status=status.HTTP_404_NOT_FOUND)
    serializer = ProdutoSerializer(instance=produto, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "produto atualizado com sucesso", "data": serializer.data})
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def excluir_vendedor(request, pk):
    try:
        vendedor = Vendedor.objects.get(pk=pk)
    except Vendedor.DoesNotExist:
        return Response({"message": "O vendedor com o ID fornecido não foi encontrado."}, status=status.HTTP_404_NOT_FOUND)
    vendedor.delete()
    return Response({"message": "Vendedor excluído com sucesso."}, status=status.HTTP_204_NO_CONTENT)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def excluir_produto(request, pk):
    try:
        produto = Produto.objects.get(pk=pk)
    except Produto.DoesNotExist:
        return Response({"message": "O produto com o ID fornecido não foi encontrado."}, status=status.HTTP_404_NOT_FOUND)
    produto.delete()
    return Response({"message": "Produto excluído com sucesso."}, status=status.HTTP_204_NO_CONTENT)

class LoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)

        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        else:
            return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)



@api_view(['POST'])
def criar_cliente(request):
    serializer = ClienteSerializer(data=request.data)
    if serializer.is_valid():
        cpf = serializer.validated_data['cpf']
        if Cliente.objects.filter(cpf=cpf).exists():
            return Response({'message': 'Cliente com CPF já existente'}, status=status.HTTP_400_BAD_REQUEST)
        if len(cpf) != 11:
             return Response({'message': 'Cpf do cliente é invalido '}, status=status.HTTP_400_BAD_REQUEST)
        try:
            serializer.save()
            return Response({"message": "Cliente foi adicionado ao banco", "data": serializer.data}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'message': f'Error saving cliente: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET'])
def listar_cliente(request, pk):
    try:
        cliente = Cliente.objects.get(pk=pk)
    except Cliente.DoesNotExist:
        return Response({"message": "O cliente não foi encontrado no banco,confira a veracidade das informações."}, status=status.HTTP_404_NOT_FOUND)
    serializer = ClienteSerializer (cliente)
    return Response(serializer.data)


@api_view(['POST'])
def atualizar_cliente(request, pk):
    try:
        cliente = Cliente.objects.get(pk=pk)
    except Cliente.DoesNotExist:
        return Response({"message": "Cliente não encontrado"}, status=status.HTTP_404_NOT_FOUND)
    serializer = ClienteSerializer(instance=cliente, data=request.data)
    if serializer.is_valid():
        cpf = serializer.validated_data['cpf']
        if Cliente.objects.filter(cpf=cpf).exists():
            return Response({'message': 'Cliente com CPF já existente'}, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response({"message": "Cliente atualizado com sucesso", "data": serializer.data})
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def excluir_cliente(request, pk):
    try:
        cliente = Cliente.objects.get(pk=pk)
    except Cliente.DoesNotExist:
        return Response({"message": "O Cliente com o ID fornecido não foi encontrado."}, status=status.HTTP_404_NOT_FOUND)
    cliente.delete()
    return Response({"message": "Cliente excluído com sucesso."}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def listar_clientes(request):
    clientes = Cliente.objects.all()
    serializer = ClienteSerializer(clientes, many=True)
    return Response(serializer.data)
