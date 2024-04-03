from rest_framework import serializers
from .models import Vendedor,Lanche
from django.db.models import fields


class vendedorSerializer(serializers.ModelSerializer):
    class Meta:
        model= Vendedor
        fields =('id','nome_vendedor','email','contato')


class lancheSerializer(serializers.ModelSerializer):
    class Meta:
        model= Lanche
        fields =('id','produto_oferecido','preçodoproduto')
