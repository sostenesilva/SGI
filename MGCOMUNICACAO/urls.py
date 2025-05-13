from django.urls import path
from . import views

urlpatterns = [
    # Demandas
    path('demandas/', views.listar_demandas, name='listar_demandas'),
    path('demandas/nova/', views.criar_demanda, name='criar_demanda'),
    path('demandas/<int:demanda_id>/editar/', views.editar_demanda, name='editar_demanda'),
    path('demandas/<int:demanda_id>/excluir/', views.excluir_demanda, name='excluir_demanda'),
    path('demandas/<int:demanda_id>/', views.detalhes_demanda, name='detalhar_demanda'),

    # Diligências
    path('demandas/<int:demanda_id>/diligencias/nova/', views.adicionar_diligencia, name='criar_diligencia'),
    path('diligencias/<int:diligencia_id>/editar/', views.editar_diligencia, name='editar_diligencia'),
    path('diligencias/<int:diligencia_id>/excluir/', views.excluir_diligencia, name='excluir_diligencia'),
]
