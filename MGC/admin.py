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
    search_fields = ('Descricao',)

@admin.register(models.EntradaSec)
class EntradaSec(admin.ModelAdmin):

    list_display = ('short_item','saldocontratosec','quantidade')
    list_filter = ('saldocontratosec',)
    search_fields = ('item','saldocontratosec')
    list_editable = ('quantidade',)

@admin.register(models.SaidaSec)
class SaidaSec(admin.ModelAdmin):

    list_display = ('short_item','saldocontratosec','quantidade')
    list_filter = ('saldocontratosec',)
    search_fields = ('item','saldocontratosec')
    list_editable = ('quantidade',)

    

admin.site.register(models.Ordem)
admin.site.register(models.SaldoContratoSec)
admin.site.register(Permission)
admin.site.register(models.Fornecedores)

