from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='mgc'),
    #path('configuracoes/', views.configuracoes, name='configuracoes'),

    # path('processos/', views.processos, name='processos'),
    # path('processos/adicionar/', views.processos_add, name='processos_add'),
    # path('processos/adicionar/licon', views.licitacao_request, name='licitacao_request'),
    # path('processos/editar/<int:processo_pk>', views.processos_edit, name='processo_edit'),
    # path('processos/deletar/<int:processo_pk>', views.processos_delet, name='processo_delet'),

    path('contratos/', views.contratos, name='contratos'), #VISUALIZAR TODOS OS CONTRATOS
    # path('contratos/adicionar/<int:processo_pk>/', views.contratos_add, name='contratos_add'),
    path('contratos/addsaldosec/<int:contrato_pk>/', views.contratos_addsaldosec, name='contrato_addsaldo'),
    path('contratos/additens/<int:contrato_pk>/', views.contratos_additens, name='contratos_additens'),
    # path('contratos/anexarof/<int:contrato_pk>/', views.contrato_enviar, name='contrato_enviar'), #ADAPTAR PARA ORDENS/ANEXAR
    # path('contratos/editar/<int:contrato_pk>', views.contrato_edit, name='contrato_edit'),
    # path('contratos/deletar/<int:contrato_pk>', views.contrato_delet, name='contrato_delet'),

    path('contratos/ordens/', views.ordens, name='ordens'),
    path('contratos/ordens/detalhes/<int:saldodetalhes_pk>/', views.saldo_detalhes, name='saldo_detalhes'),
    path('contratos/ordens/detalhes/<int:saldodetalhes_pk>/emitir', views.of_emitir, name='of_emitir'),

    path('contratos/ordens/detalhes/<int:saldoof_pk>/<int:of_log_pk>', views.of_log_delet, name='of_log_delet'),
    path('contratos/ordens/editar/<int:saldoof_pk>', views.of_edit, name='of_edit'),
    #path('contratos/ordens/deletar/<int:saldoof_pk>', views.of_delet, name='of_delet'),

    path('contratos/fiscal/', views.painelfiscal, name='painelfiscal'),

    path('contratos/adicionar', views.add_contratos, name='add_contratos'),
    path('contratos/editar/<int:contrato_id>', views.edit_contrato, name='edit_contrato'),
    path('contratos/request', views.contratos_request, name='contratos_request'),
    path('contratos/resquest/processar', views.processar_contratos_selecionados, name='processar_contratos_selecionados'),

    path('fornecedor/editar/<int:saldocontratosec_id>', views.confirmar_fornecedor, name='confirmar_fornecedor'),

    path('saldosec/<int:saldocontratosec_id>/exportar_excel/', views.exportar_excel_saldo, name='exportar_excel_saldo'),

    path('emitirof', views.emitirOF, name='emitirof'),

    #### HTMX ###########

    path('contratosbase/', views.contratos_base, name='contratos_base'),

    
    
]