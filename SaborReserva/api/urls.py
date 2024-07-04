from django.urls import path
from . import views
from .views import LoginAPIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('', views.api_geral, name='home_api'),

    path('criar/vendedor', views.criar_vendedor, name='adiciona_vendedor'),
    path('criar/produto',views.criar_produto,name='adiciona_produto'),
    path('criar/cliente',views.criar_cliente,name='adiciona_cliente'),

    path('listar/clientes', views.listar_clientes, name='listar_clientes'),
    path('listar/vendedores', views.listar_vendedores, name='listar_vendedores'),
    path('listar/produtos', views.listar_produtos, name='listar_produtos'),

    path('listar/vendedor', views.listar_vendedor, name='listar_vendedor'),
    path('listar/produto/<int:pk>', views.listar_produto, name='listar_produto'),
    path('listar/cliente/<int:pk>', views.listar_cliente, name='listar_cliente'),
    path('listar/produto_vendedor', views.listar_produtos_vendedor, name='listar_produtos_vendedor'),

    path('atualizar/vendedor', views.atualizar_vendedor, name='atualizar_vendedor'),
    path('atualizar/produto/<int:pk>/', views.atualizar_produto, name='atualizar_produto'),
    path('atualizar/cliente/<int:pk>', views.atualizar_cliente, name='atualizar_cliente'),

    path('excluir/vendedor', views.deletar_vendedor, name='excluir_vendedor'),
    path('excluir/produto', views.excluir_produto, name='excluir_produto'),
    path('excluir/cliente/<int:pk>', views.excluir_cliente, name='excluir_cliente'),

    path('api/token/', LoginAPIView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
