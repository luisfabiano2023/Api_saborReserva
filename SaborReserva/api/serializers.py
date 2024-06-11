from rest_framework import serializers
from .models import Vendedor, Produto, Cliente

class VendedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendedor
        fields = ('id', 'nome_vendedor', 'email_vendedor', 'telefone_vendedor', 'cpf_cnpj_vendedor', 'link_contato')
        read_only_fields = ('id',)

class ProdutoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produto
        fields = ('id_produto', 'nome_produto', 'preco_produto', 'descricao_produto', 'categoria', 'status_produto', 'foto_produto')
        read_only_fields = ('id_produto',)

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = ('id','nome_cliente', 'endereco_cliente','contato_cliente','cpf') 
        read_only_fields = ('id',)
