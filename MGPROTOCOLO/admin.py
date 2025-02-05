from django.contrib import admin
from . import models

admin.site.register(models.Documento)
admin.site.register(models.Movimentacao)
admin.site.register(models.Setor)
admin.site.register(models.Processo)
