from rest_framework import serializers
from .models import Vendedor, Lanche

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

