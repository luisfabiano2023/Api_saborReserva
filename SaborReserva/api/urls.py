from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('', views.api_geral, name='home_api'),
    path('criar/vendedor', views.criar_vendedor, name='adiciona_vendedor'),
    path('criar/lanche',views.criar_lanche,name='adiciona_lanche'),
    path('listar/vendedores', views.listar_vendedores, name='listar_vendedores'),
    path('listar/lanches', views.listar_lanches, name='listar_lanches'),
    path('listar/vendedor/<int:pk>', views.listar_vendedor, name='listar_vendedor'),
    path('listar/lanche/<int:pk>', views.listar_lanche, name='listar_lanche'),
    path('atualizar/vendedor/<int:pk>', views.atualizar_vendedor, name='atualizar_vendedor' ),
    path('atualizar/lanche/<int:pk>', views.atualizar_lanche, name='atualizar_lanche'),
    path('excluir/vendedor/<int:pk>', views.excluir_vendedor, name='excluir_vendedor'),
    path('excluir/lanche/<int:pk>', views.excluir_lanche, name='excluir_lanche'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
