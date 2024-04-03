from django.db import models


class Vendedor(models.Model):
    nome_vendedor = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    contato = models.CharField(max_length=20)
    
    def __str__(self):
      return self.nome_vendedor
    
    

class Lanche(models.Model):
    produto_oferecido = models.CharField(max_length=255)
    preçodoproduto= models.DecimalField( max_digits=10, decimal_places=2, default=0.00)