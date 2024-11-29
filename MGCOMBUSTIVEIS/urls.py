from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashcombustiveis, name='dashcombustiveis'),
    path('abastecimentos/', views.abastecimentos, name='abastecimentos'),

]