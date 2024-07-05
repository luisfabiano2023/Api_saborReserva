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
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.decorators import api_view, parser_classes, permission_classes
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from .serializers import CustomTokenObtainPairSerializer
from rest_framework.authtoken.models import Token



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
@permission_classes([AllowAny])
def criar_vendedor(request):
    serializer = VendedorSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Vendedor criado com sucesso", "data": serializer.data}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def atualizar_vendedor(request):
    print("Dados recebidos:", request.data)  # Log dos dados recebidos
    try:
        vendedor = Vendedor.objects.get(user=request.user)
    except Vendedor.DoesNotExist:
        return Response({"detail": "Vendedor não encontrado."}, status=status.HTTP_404_NOT_FOUND)

    data = request.data.copy()

    # Verificar se o email mudou
    if vendedor.user.email == data.get('user', {}).get('email'):
        # Email não mudou, remover do data para ignorar a verificação de unicidade
        data.get('user', {}).pop('email', None)

    serializer = VendedorSerializer(vendedor, data=data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Vendedor atualizado com sucesso", "data": serializer.data})
    else:
        print("Erros de validação:", serializer.errors)  # Log dos erros de validação
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def deletar_vendedor(request):
    user = request.user
    vendedor = get_object_or_404(Vendedor, user=user)
    vendedor.delete()
    return Response({"message": "Vendedor deletado com sucesso"}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def listar_vendedores(request):
    vendedores = Vendedor.objects.all()
    serializer = VendedorSerializer(vendedores, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def listar_vendedor(request):
    user = request.user
    try:
        vendedor = Vendedor.objects.get(user=user)
    except Vendedor.DoesNotExist:
        return Response({"message": "Vendedor não encontrado."}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = VendedorSerializer(vendedor)
    return Response(serializer.data)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def criar_produto(request):
    user = request.user
    try:
        vendedor = Vendedor.objects.get(user=user)
    except Vendedor.DoesNotExist:
        return Response({"detail": "Vendedor não encontrado."}, status=status.HTTP_404_NOT_FOUND)
    
    data = request.data.copy()
    print("Dados recebidos para criação do produto:", data)
    data['vendedor'] = vendedor.id  # Adiciona o ID do vendedor nos dados
    
    serializer = ProdutoSerializer(data=data)
    if serializer.is_valid():
        serializer.save(vendedor=vendedor)  # Certifica-se de salvar com o vendedor correto
        return Response({"message": "Produto criado com sucesso", "data": serializer.data}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def atualizar_produto(request, pk):
    user = request.user
    vendedor = get_object_or_404(Vendedor, user=user)
    produto = get_object_or_404(Produto, pk=pk, vendedor=vendedor)
    
    serializer = ProdutoSerializer(instance=produto, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Produto atualizado com sucesso", "data": serializer.data})
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def excluir_produto(request, pk):
    user = request.user
    vendedor = get_object_or_404(Vendedor, user=user)
    produto = get_object_or_404(Produto, pk=pk, vendedor=vendedor)
    produto.delete()
    return Response({"message": "Produto excluído com sucesso"}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def listar_produtos(request):
    produtos = Produto.objects.all()
    serializer = ProdutoSerializer(produtos, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def listar_produto(request, pk):
    try:
        produto = Produto.objects.get(pk=pk)
    except produto.DoesNotExist:
        return Response({"message": "O produto com o ID fornecido não foi encontrado."}, status=status.HTTP_404_NOT_FOUND)
    serializer = ProdutoSerializer(produto)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def listar_produtos_vendedor(request):
    user = request.user
    vendedor = get_object_or_404(Vendedor, user=user)
    produtos = Produto.objects.filter(vendedor=vendedor)
    
    serializer = ProdutoSerializer(produtos, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


class LoginAPIView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        # Usa o serializer personalizado para validar os dados e gerar o token
        serializer = CustomTokenObtainPairSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)


User = get_user_model()

class LoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        # Busca o usuário pelo email
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        # Verifica a senha
        if user.check_password(password):
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        else:
            return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)




@api_view(['POST'])
@permission_classes([IsAuthenticated])
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
@permission_classes([IsAuthenticated])
def listar_cliente(request, pk):
    try:
        cliente = Cliente.objects.get(pk=pk)
    except Cliente.DoesNotExist:
        return Response({"message": "O cliente não foi encontrado no banco,confira a veracidade das informações."}, status=status.HTTP_404_NOT_FOUND)
    serializer = ClienteSerializer (cliente)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
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
@permission_classes([IsAuthenticated])
def excluir_cliente(request, pk):
    try:
        cliente = Cliente.objects.get(pk=pk)
    except Cliente.DoesNotExist:
        return Response({"message": "O Cliente com o ID fornecido não foi encontrado."}, status=status.HTTP_404_NOT_FOUND)
    cliente.delete()
    return Response({"message": "Cliente excluído com sucesso."}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def listar_clientes(request):
    clientes = Cliente.objects.all()
    serializer = ClienteSerializer(clientes, many=True)
    return Response(serializer.data)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def excluir_vendedor(request, pk):
    try:
        vendedor = Vendedor.objects.get(pk=pk)
    except Vendedor.DoesNotExist:
        return Response({"message": "O vendedor com o ID fornecido não foi encontrado."}, status=status.HTTP_404_NOT_FOUND)
    vendedor.delete()
    return Response({"message": "Vendedor excluído com sucesso."}, status=status.HTTP_204_NO_CONTENT)
