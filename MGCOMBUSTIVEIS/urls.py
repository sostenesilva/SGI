from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashcombustiveis, name='dashcombustiveis'),
    path('abastecimentos/', views.abastecimentos, name='abastecimentos'),
    path('abastecimentos/list', views.abastecimentos_list, name='abastecimentos_list'),
    path('abastecimentos/add', views.add_abastecimento, name='add_abastecimento'),
    path('abastecimentos/<int:abastecimento_pk>/edit', views.edit_abastecimento, name='edit_abastecimento'),

]