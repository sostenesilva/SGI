from django.urls import path
from . import views


urlpatterns = [
    path('', views.listar_documentos, name='listar_documentos'),
    path('registrar/', views.registrar_documento, name='registrar_documento'),
    path('tramitar/<int:documento_id>/', views.registrar_movimentacao, name='registrar_movimentacao'),
    path('concluir/<int:documento_id>/', views.concluir_documento, name='concluir_documento'),
    path('relatorio/emitir/', views.emitir_relatorio_protocolo, name='emitir_relatorio_protocolo'),  # Relatório
    path('relatorio/upload/<int:relatorio_id>/', views.upload_relatorio, name='upload_relatorio'),  # Upload
    path('movimentacoes/consultar/', views.consultar_movimentacao, name='consultar_movimentacao'),  # Consulta
    path('movimentacoes/', views.listar_movimentacoes_em_tramitacao, name='listar_movimentacoes_em_tramitacao'),
    path('protocolo/emitir/<int:protocolo_id>/', views.emitir_protocolo, name='emitir_protocolo'),
    path('protocolos/pendentes/', views.listar_protocolos_pendentes, name='listar_protocolos_pendentes'),
    path('protocolo/finalizar/<int:protocolo_id>/', views.finalizar_protocolo, name='finalizar_protocolo'),
]
