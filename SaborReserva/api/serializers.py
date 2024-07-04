from rest_framework import serializers
from .models import Vendedor, Produto, Cliente, CustomUser
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Adiciona o email no payload do token
        token['email'] = user.email
        return token

    def validate(self, attrs):
        # Substitui a validação padrão para aceitar email e senha
        email = attrs.get('email')
        password = attrs.get('password')

        # Busca o usuário pelo email
        user = authenticate(email=email, password=password)
        if user is not None:
            refresh = self.get_token(user)

            data = {}
            data['refresh'] = str(refresh)
            data['access'] = str(refresh.access_token)

            return data
        else:
            raise serializers.ValidationError('Invalid email or password')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user

    def update(self, instance, validated_data):
        new_email = validated_data.get('email', instance.email)
        
        # Verifica se o email está sendo atualizado e se pertence a outro usuário
        if new_email != instance.email and CustomUser.objects.filter(email=new_email).exists():
            raise serializers.ValidationError({'email': 'Este email já está em uso.'})

        instance.username = validated_data.get('username', instance.username)
        instance.email = new_email
        instance.save()
        return instance

class VendedorSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Vendedor
        fields = ['user', 'telefone_vendedor', 'cpf_cnpj_vendedor', 'link_contato']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = CustomUser.objects.create_user(**user_data)
        vendedor = Vendedor.objects.create(user=user, **validated_data)
        return vendedor

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', None)
        if user_data:
            user_serializer = UserSerializer(instance.user, data=user_data, partial=True)
            if user_serializer.is_valid():
                user_serializer.save()
            else:
                raise serializers.ValidationError(user_serializer.errors)

        instance.telefone_vendedor = validated_data.get('telefone_vendedor', instance.telefone_vendedor)
        instance.cpf_cnpj_vendedor = validated_data.get('cpf_cnpj_vendedor', instance.cpf_cnpj_vendedor)
        instance.link_contato = validated_data.get('link_contato', instance.link_contato)
        instance.save()
        return instance

class ProdutoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produto
        fields = ['id_produto', 'nome_produto', 'preco_produto', 'descricao_produto', 'categoria', 'status_produto', 'foto_produto']

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = ['id', 'nome_cliente', 'email', 'contato_cliente', 'cpf']
        read_only_fields = ['id']
