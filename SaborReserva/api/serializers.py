from rest_framework import serializers
from .models import Vendedor, Lanche,Cliente

class VendedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendedor
        fields = ('id', 'nome_vendedor', 'email', 'contato')
        read_only_fields = ('id',)

class LancheSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lanche
        fields = ('id', 'produto_oferecido', 'preçodoproduto')
        read_only_fields = ('id',)

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = ('id','nome_cliente', 'email','contato_cliente','cpf') 
        read_only_fields = ('id',)
