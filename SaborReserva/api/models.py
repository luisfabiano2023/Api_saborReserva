from django.db import models


class Vendedor(models.Model):
    nome_vendedor = models.CharField(max_length=255)
    email_vendedor = models.CharField(max_length=255, default='email@example.com')
    telefone_vendedor = models.CharField(max_length=20, default='0000000000')
    cpf_cnpj_vendedor = models.CharField(max_length=20, default='00000000000')
    link_contato = models.URLField(max_length=255, default='http://example.com')

    def __str__(self):
        return self.nome_vendedor
    

def upload_foto_produto(instance, filename):
    return f"{instance.id_produto}-{filename}"


class Produto(models.Model):
    id_produto = models.AutoField(primary_key=True)
    nome_produto = models.CharField(max_length=255)
    preco_produto = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    descricao_produto = models.TextField()
    categoria = models.CharField(max_length=255)
    status_produto = models.CharField(max_length=255)
    foto_produto = models.ImageField(upload_to=upload_foto_produto, blank=True, null=True)

    def __str__(self):
        return self.nome_produto


class Cliente(models.Model):
    nome_cliente = models.CharField(max_length=255)
    email= models.CharField(max_length=255)
    contato_cliente = models.CharField(max_length=20)
    cpf = models.CharField(max_length=11)
    
    def __str__(self):
      return self.nome_cliente
