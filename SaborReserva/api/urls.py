from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('', views.api_geral, name='home_api'),

    path('criar/vendedor', views.criar_vendedor, name='adiciona_vendedor'),
    path('criar/lanche',views.criar_lanche,name='adiciona_lanche'),
    path('criar/cliente',views.criar_cliente,name='adiciona_lanche'),

    path('listar/clientes', views.listar_clientes, name='listar_lanches'),
    path('listar/vendedores', views.listar_vendedores, name='listar_vendedores'),
    path('listar/lanches', views.listar_lanches, name='listar_lanches'),

    path('listar/vendedor/<int:pk>', views.listar_vendedor, name='listar_vendedor'),
    path('listar/lanche/<int:pk>', views.listar_lanche, name='listar_lanche'),
    path('listar/cliente/<int:pk>', views.listar_cliente, name='listar_cliente'),

    path('atualizar/vendedor/<int:pk>', views.atualizar_vendedor, name='atualizar_vendedor' ),
    path('atualizar/lanche/<int:pk>', views.atualizar_lanche, name='atualizar_lanche'),
    path('atualizar/cliente/<int:pk>', views.atualizar_cliente, name='atualizar_cliente'),

    path('excluir/vendedor/<int:pk>', views.excluir_vendedor, name='excluir_vendedor'),
    path('excluir/lanche/<int:pk>', views.excluir_lanche, name='excluir_lanche'),
    path('excluir/cliente/<int:pk>', views.excluir_cliente, name='excluir_cliente'),

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
