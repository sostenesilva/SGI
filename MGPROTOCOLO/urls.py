from django.urls import path
from . import views

urlpatterns = [
    path('', views.processos_no_setor, name='protocolo_inicial'),
    path('processos/no-setor/', views.processos_no_setor, name='processos_no_setor'),
    path('processos/encaminhados/', views.processos_encaminhados_pelo_setor, name='processos_encaminhados_pelo_setor'),
    path('processos/<int:processo_id>/', views.detalhes_processo, name='detalhes_processo'),
    path('processos/criar/', views.criar_processo, name='criar_processo'),
    path('processos/editar/<int:processo_id>/', views.editar_processo, name='editar_processo'),
    path('processos/<int:processo_id>/documentos/criar/', views.criar_documento, name='criar_documento'),
    path('processos/<int:processo_id>/maisinformacoes/', views.mais_informacoes, name='mais_informacoes'),
    
    path('movimentacoes/<int:processo_id>/criar/', views.criar_movimentacao, name='criar_movimentacao'),
    path('movimentacoes/tramitacao/', views.listar_movimentacoes_tramitacao, name='listar_movimentacoes_tramitacao'),

    path('processo/<int:processo_id>/receber/', views.receber_processo, name='receber_processo'),
    path('processo/<int:processo_id>/arquivar/', views.arquivar_processo, name='arquivar_processo'),
    path('processos-arquivados/', views.processos_arquivados, name='processos_arquivados'),


    path('protocolos/gerar/', views.gerar_protocolo, name='gerar_protocolo'),
    path('protocolos/', views.listar_protocolos, name='listar_protocolos'),
    path('protocolos/<int:protocolo_id>/comprovacao/', views.anexar_comprovacao, name='anexar_comprovacao'),
    path('protocolos/<int:protocolo_id>/comprovacao/visualizar/', views.visualizar_comprovacao, name='visualizar_comprovacao'),
]