from django.contrib import admin
from . import models

@admin.register(models.Secretaria)
class Secretaria(admin.ModelAdmin):
    list_display = ('nome','sigla','ativo')
    list_editable = ('ativo',)

@admin.register(models.Setor)
class Setor(admin.ModelAdmin):
    list_display = ('nome','sigla', 'secretaria','ativo')
    list_editable = ('ativo',)

@admin.register(models.Modulo)
class Modulo(admin.ModelAdmin):
    list_display = ('nome', 'permissao')

@admin.register(models.Tutorial)
class Tutorial(admin.ModelAdmin):
    list_display = ('titulo','modulo')

@admin.register(models.Notificacao)
class Notificacao(admin.ModelAdmin):
    list_display = ('titulo', 'usuario', 'lida', 'criada_em')
