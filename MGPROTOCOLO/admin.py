from django.contrib import admin
from . import models

admin.site.register(models.Documento)

@admin.register(models.Movimentacao)
class Movimentacao(admin.ModelAdmin):
    list_display = ('processo', 'realizado_por', 'realizado_em', 'destinatario','confirmacao')

@admin.register(models.Processo)
class Processo(admin.ModelAdmin):
    list_display = ('numero','descricao','atual')

    
@admin.register(models.CorrecaoProcesso)
class CorrecaoProcesso(admin.ModelAdmin):
    list_display = ('processo','campo_alterado','usuario','data')

admin.site.register(models.ProtocoloMovimentacao)
