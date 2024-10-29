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

    path('contratos/', views.contratos, name='contratos'),
    # path('contratos/adicionar/<int:processo_pk>/', views.contratos_add, name='contratos_add'),
    path('contratos/addof/<int:contrato_pk>/', views.contratos_add_of, name='contrato_add_of'),
    path('contratos/additens/<int:contrato_pk>/', views.contratos_additens, name='contratos_additens'),
    # path('contratos/anexarof/<int:contrato_pk>/', views.contrato_enviar, name='contrato_enviar'), #ADAPTAR PARA ORDENS/ANEXAR
    # path('contratos/editar/<int:contrato_pk>', views.contrato_edit, name='contrato_edit'),
    # path('contratos/deletar/<int:contrato_pk>', views.contrato_delet, name='contrato_delet'),

    path('contratos/ordens/', views.ordens, name='ordens'),
    path('contratos/ordens/detalhes/<int:saldoof_pk>/', views.of_enviar, name='of_enviar'),
    path('contratos/ordens/detalhes/<int:saldoof_pk>/emitir', views.of_emitir, name='of_emitir'),
    path('contratos/ordens/detalhes/<int:saldoof_pk>/emitirdoc', views.emitirDocOf, name='emitirDocOf'),

    path('contratos/ordens/detalhes/<int:saldoof_pk>/<int:of_log_pk>', views.of_log_delet, name='of_log_delet'),
    path('contratos/ordens/editar/<int:saldoof_pk>', views.of_edit, name='of_edit'),
    #path('contratos/ordens/deletar/<int:saldoof_pk>', views.of_delet, name='of_delet'),

    path('contratos/fiscal/', views.painelfiscal, name='painelfiscal'),


    path('contratos/request', views.contratos_request, name='contratos_request'),


    # path('criterios/', views.criterios, name='criterios'),
    # path('criterios/adicionar/', views.criterios_add, name='criterios_add'),
    # path('criterios/editar/<int:criterio_pk>', views.criterios_edit, name='criterios_edit'),
    # path('criterios/deletar/<int:criterio_pk>', views.criterios_delet, name='criterios_delet'),

    # path('controle/', views.controle, name='controle'),
    # path('secadm/', views.secadm, name='secadm'),
    
]