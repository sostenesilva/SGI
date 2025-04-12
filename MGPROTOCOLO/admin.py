from django.contrib import admin
from . import models

admin.site.register(models.Documento)

@admin.register(models.Movimentacao)
class Movimentacao(admin.ModelAdmin):
    list_display = ('processo', 'realizado_por', 'realizado_em', 'setor_destino','confirmacao')

admin.site.register(models.Setor)

@admin.register(models.Processo)
class Processo(admin.ModelAdmin):
    list_display = ('numero','descricao','setor_atual')
    list_editable = ('descricao',)

admin.site.register(models.ProtocoloMovimentacao)
