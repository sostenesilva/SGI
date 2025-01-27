from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashcombustiveis, name='dashcombustiveis'),
    path('abastecimentos/', views.abastecimentos, name='abastecimentos'),
    path('abastecimentos/list', views.abastecimentos_list, name='abastecimentos_list'),
    path('abastecimentos/add', views.add_abastecimento, name='add_abastecimento'),
    path('abastecimentos/<int:abastecimento_pk>/edit', views.edit_abastecimento, name='edit_abastecimento'),
    path('frota/', views.frota, name='frota'),
    path('frota/list', views.frota_list, name='frota_list'),
    path('frota/add', views.add_frota, name='add_frota'),
    path('frota/<int:frota_pk>/edit', views.edit_frota, name='edit_frota'),
    path('condutores/', views.condutores, name='condutores'),
    path('condutores/list', views.condutores_list, name='condutores_list'),
    path('condutores/add', views.add_condutores, name='add_condutores'),
    path('condutores/<int:condutor_pk>/edit', views.edit_condutores, name='edit_condutores'),
    path('relatorios/', views.emitir_relatorio, name='emitir_relatorio'),
]