from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Vendedor, Lanche,Cliente
from .serializers import VendedorSerializer, LancheSerializer,ClienteSerializer
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
        'Criar Lanche': 'criar/lanche',
        'Listar Vendedores': 'listar/vendedores',
        'Listar Lanches': 'listar/lanches',
        'Listar Vendedor': 'listar/vendedor/<int:pk>',
        'Listar Lanche': 'listar/lanche/<int:pk>',
        'Atualizar Vendedor': 'atualizar/vendedor/<int:pk>',
        'Atualizar Lanche': 'atualizar/lanche/<int:pk>',
        'Excluir Vendedor': 'excluir/vendedor/<int:pk>',
        'Excluir Lanche': 'excluir/lanche/<int:pk>',
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
def criar_lanche(request):
    serializer = LancheSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Lanche criado com sucesso", "data": serializer.data}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def listar_vendedores(request):
    vendedores = Vendedor.objects.all()
    serializer = VendedorSerializer(vendedores, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def listar_lanches(request):
    lanches = Lanche.objects.all()
    serializer = LancheSerializer(lanches, many=True)
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
def listar_lanche(request, pk):
    try:
        lanche = Lanche.objects.get(pk=pk)
    except Lanche.DoesNotExist:
        return Response({"message": "O lanche com o ID fornecido não foi encontrado."}, status=status.HTTP_404_NOT_FOUND)
    serializer = LancheSerializer(lanche)
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
def atualizar_lanche(request,pk):
    try:
        lanche = Lanche.objects.get(pk=pk)
    except Lanche.DoesNotExist:
        return Response({"message": "Lanche não encontrado"}, status=status.HTTP_404_NOT_FOUND)
    serializer = LancheSerializer(instance=lanche, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Lanche atualizado com sucesso", "data": serializer.data})
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
def excluir_lanche(request, pk):
    try:
        lanche = Lanche.objects.get(pk=pk)
    except Lanche.DoesNotExist:
        return Response({"message": "O lanche com o ID fornecido não foi encontrado."}, status=status.HTTP_404_NOT_FOUND)
    lanche.delete()
    return Response({"message": "Lanche excluído com sucesso."}, status=status.HTTP_204_NO_CONTENT)

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
        # Check for duplicate CPF
        cpf = serializer.validated_data['cpf']
        if Cliente.objects.filter(cpf=cpf).exists():
            return Response({'message': 'Cliente com CPF já existente'}, status=status.HTTP_400_BAD_REQUEST)

        # Save the serializer and handle potential errors
        try:
            serializer.save()
            return Response({"message": "Cliente foi adicionado ao banco", "data": serializer.data}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'message': f'Error saving cliente: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    return   

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
