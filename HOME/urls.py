from django.urls import path
from . import views

urlpatterns = [
    path('', views.portal_inicial, name='portal_inicial'),
    path('modulo/<int:modulo_id>/', views.modulo_detalhes, name='modulo_detalhes'),
    path('modulo/<int:modulo_id>/', views.modulo_detalhes, name='modulo_detalhes'),
    path('grupos/', views.grupos_permissoes, name='grupos_permissoes'),
    path('usuarios/', views.listar_usuarios, name='listar_usuarios'),
    path('privilegios/<int:user_id>/', views.privilegios, name='privilegios'),
    path("privilegios/<int:user_id>/<int:grupo_id>/", views.carregar_permissoes, name="carregar_permissoes"),
    path("privilegios/<int:user_id>/<int:grupo_id>/<int:permissao_id>/", views.atualizar_permissao_usuario, name="atualizar_permissao_usuario"),

]