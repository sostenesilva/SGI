from django.urls import path
from . import views

urlpatterns = [
    path('', views.portal_inicial, name='portal_inicial'),
    path('modulo/<int:modulo_id>/', views.modulo_detalhes, name='modulo_detalhes'),
    path('modulo/<int:modulo_id>/', views.modulo_detalhes, name='modulo_detalhes'),
]