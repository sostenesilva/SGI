from django.contrib import admin
from . import models

admin.site.register(models.DbDimensao)
admin.site.register(models.DbCriterios)
admin.site.register(models.DbAvaliacao)
admin.site.register(models.DbAvaliacaoLog)
