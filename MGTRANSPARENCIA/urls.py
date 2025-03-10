from django.urls import path
from . import views

urlpatterns = [
    path("criterios/", views.listar_criterios, name="listar_criterios"),
    path("criterios/<int:criterio_id>/informacao/", views.informacoes_criterios, name="informacoes_criterios"),
    path("", views.listar_avaliacoes, name="listar_avaliacoes"),
    path("avaliacoes/<int:avaliacao_id>/", views.detalhes_avaliacao, name="detalhes_avaliacao"),
    path("avaliacoes/adicionar/", views.adicionar_avaliacao, name="adicionar_avaliacao"),
    path("avaliacoes/<int:avaliacao_id>/tarefa/adicionar", views.adicionar_tarefa, name="adicionar_tarefa"),
    path("avaliacoes/tarefa/<int:tarefa_id>/editar", views.editar_tarefa, name="editar_tarefa"),
    path('documento/<int:log_id>/enviar/', views.enviar_documento_log, name='enviar_documento_log'),
    path('documento/<int:log_id>/aprovar/', views.aprovar_documento, name='aprovar_documento'),
    path('documento/<int:log_id>/apagararquivo/', views.apagar_documento_log, name='apagar_documento_log'),
    path('addcriterios/', views.importar_criterios, name='importar_criterios'),
]