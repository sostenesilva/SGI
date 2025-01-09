from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashregularidade, name='dashregularidadefiscal'),
    path('consulta', views.consulta_externa, name='consulta_externa'),
    path('consulta/dadosdeclaracao', views.dadosdeclaracao_externa, name='dadosdeclaracao_externa'),
    path('fornecedoreslist/', views.fornecedores_list, name='fornecedores_list'),
    path('certidoeslist/<int:fornecedor_id>/', views.certidoes_list, name='certidoes_list'),
    path('declaracoeslist/<int:fornecedor_id>/', views.declaracoes_list, name='declaracoes_list'),
    path('regularidaderesumo/<int:fornecedor_id>/', views.regularidade_resumo, name='regularidade_resumo'),
    path('adicionarcertidoes/<int:fornecedor_id>/', views.certidoes_add, name='certidoes_add'),
    path('emitirdeclaracao/<int:fornecedor_id>/', views.emitir_declaracao, name='emitir_declaracao'),
]