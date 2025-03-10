from django.contrib import admin
from . import models

admin.site.register(models.DbDimensao)
admin.site.register(models.DbAvaliacao)
admin.site.register(models.DbAvaliacaoLog)
admin.site.register(models.InformacoesCriterio)


@admin.register(models.DbCriterios)
class DbCriterios(admin.ModelAdmin):
    list_display = ('item', 'criterio','dimensao','periodicidade')
    list_editable = ('dimensao','periodicidade')
    list_display_links =('item', 'criterio')
    # list_filter = ('AnoContrato', 'UnidadeGestora')