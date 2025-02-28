from django.contrib import admin
from . import models

admin.site.register(models.DbDimensao)
admin.site.register(models.DbAvaliacao)
admin.site.register(models.DbAvaliacaoLog)


@admin.register(models.DbCriterios)
class DbCriterios(admin.ModelAdmin):
    # list_display = ('NumeroContrato','AnoContrato','TipoProcesso','NumeroProcesso','AnoProcesso','Fornecedor')
    list_editable = ('dimensao','periodicidade')
    # list_filter = ('AnoContrato', 'UnidadeGestora')