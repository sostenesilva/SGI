# Generated by Django 4.2.16 on 2025-04-12 13:38

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('HOME', '0008_modulo_permissao_setor_notificacao'),
    ]

    operations = [
        migrations.AlterField(
            model_name='setor',
            name='usuarios',
            field=models.ManyToManyField(blank=True, null=True, to=settings.AUTH_USER_MODEL),
        ),
    ]
