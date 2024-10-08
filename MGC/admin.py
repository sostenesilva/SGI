from django.contrib import admin
from django.contrib.auth.models import Permission

from . import models

admin.site.register(models.Contratos)
admin.site.register(models.EntradaSec)
admin.site.register(models.Ordem)
admin.site.register(models.Itens)
admin.site.register(models.SaldoContratoSec)
admin.site.register(Permission)

