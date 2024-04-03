from django.urls import path
from . import views
from .views import MinhaAPIView


urlpatterns = [
	path('', views.api_geral, name='home_api'),
    path('listar/vendedores', views.listar_vendedores, name='listar_vendedores'),
    path('listar/lanches', views.listar_lanches, name='listar_lanches'),
    path('listar/vendedor/<int:pk>/', views.listar_vendedor, name='listar_vendedor'),
    path('listar/lanche/<int:pk>/', views.listar_lanche, name='listar_lanche'),
    path('create/vendedor', views.criar_vendedor, name='adiciona_vendedor'),
    path('create/lanche',views.criar_lanche,name='adiciona_lanche'),
    path('minha-api/', MinhaAPIView.as_view(), name='minha-api'),
]
