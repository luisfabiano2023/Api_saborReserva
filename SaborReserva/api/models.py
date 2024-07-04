from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.core.validators import RegexValidator

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    username_validator = RegexValidator(
        regex=r'^[\w\s.@+-]+$',
        message='Enter a valid username. This value may contain only letters, numbers, spaces, and @/./+/-/_ characters.',
    )

    username = models.CharField(
        max_length=150,
        help_text='Required. 150 characters or fewer. Letters, digits, spaces, and @/./+/-/_ only.',
        validators=[username_validator],
        unique=False  # Remove a unicidade do username
    )

    USERNAME_FIELD = 'email'  # Define o email como USERNAME_FIELD
    REQUIRED_FIELDS = ['username']


class Vendedor(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Relacionamento um-para-um com User
    telefone_vendedor = models.CharField(max_length=20, default='0000000000')
    cpf_cnpj_vendedor = models.CharField(max_length=20, default='00000000000')
    link_contato = models.URLField(max_length=255, default='http://example.com')

    def __str__(self):
        return self.user.username  # Retorna o nome de usuário como string representativa

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
    vendedor = models.ForeignKey(Vendedor, on_delete=models.CASCADE, related_name='produtos')

    def __str__(self):
        return self.nome_produto

class Cliente(models.Model):
    nome_cliente = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    contato_cliente = models.CharField(max_length=20)
    cpf = models.CharField(max_length=11)

    def __str__(self):
        return self.nome_cliente