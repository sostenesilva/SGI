from django.urls import path
from . import views

urlpatterns = [
    path('', views.atalhos, name='atalhos'),
]