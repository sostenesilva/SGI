from django.contrib import admin
from django.contrib.auth.models import Permission

from . import models

@admin.register(models.Contratos)
class Contratos(admin.ModelAdmin):
    list_display = ('NumeroContrato','AnoContrato','TipoProcesso','NumeroProcesso','AnoProcesso','Fornecedor')
    # list_editable = ('TipoProcesso','NumeroProcesso','AnoProcesso')
    list_filter = ('AnoContrato', 'UnidadeGestora')

@admin.register(models.Itens)
class Itens(admin.ModelAdmin):
    list_display = ('Descricao','Contrato')
    list_filter = ('Contrato',)


admin.site.register(models.EntradaSec)
admin.site.register(models.Ordem)
admin.site.register(models.SaldoContratoSec)
admin.site.register(Permission)
admin.site.register(models.Fornecedores)

