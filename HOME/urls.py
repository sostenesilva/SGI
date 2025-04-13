from django.urls import path
from . import views

urlpatterns = [
    path('portalantigo/', views.portal_inicial, name='portal_inicial'),
    path('', views.novoportal, name='novoportal'),
    path('modulo/<int:modulo_id>/', views.modulo_detalhes, name='modulo_detalhes'),
    path('modulo/<int:modulo_id>/', views.modulo_detalhes, name='modulo_detalhes'),
    
    path('usuarios/', views.listar_usuarios, name='listar_usuarios'),
    path('usuarios/permissoes/<int:user_id>/', views.permissoes, name='permissoes'),
    path("privilegios/<int:user_id>/<int:permissao_id>/", views.atualizar_permissao_usuario, name="atualizar_permissao_usuario"),

    path("notificacoes/listar_todas/<int:user_id>", views.listar_notificacoes, name="listar_notificacoes"),

    path("notificacoes/quantidade/", views.notificacoes_quantidade, name="notificacoes_quantidade"),
    path("notificacoes/conteudo/", views.notificacoes_conteudo, name="notificacoes_conteudo"),

]