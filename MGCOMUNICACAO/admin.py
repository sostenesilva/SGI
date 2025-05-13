from django.contrib import admin
from .models import Demanda, Diligencia

class DiligenciaInline(admin.TabularInline):
    model = Diligencia
    extra = 0

@admin.register(Demanda)
class DemandaAdmin(admin.ModelAdmin):
    list_display = ('documento_motivador', 'prazo_geral')
    search_fields = ('documento_motivador', 'descricao')
    list_filter = ('prazo_geral',)
    inlines = [DiligenciaInline]

@admin.register(Diligencia)
class DiligenciaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'prazo', 'status', 'demanda')
    search_fields = ('titulo', 'descricao', 'status')
    list_filter = ('prazo', 'status')
