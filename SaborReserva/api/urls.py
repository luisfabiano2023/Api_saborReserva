from django.urls import path
from . import views


urlpatterns = [
	path('', views.api_geral, name='home_api'),
    path('all_vendedores/', views.listar_vendedores, name='listar_vendedores'),
    path('all_lanches/', views.listar_lanches, name='listar_lanches'),
    path('create/vendedor', views.criar_vendedor, name='adicionaVendedor'),
    path('create/lanche',views.criar_lanche,name='adicionaLanche')
]