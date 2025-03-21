# Generated by Django 4.2.16 on 2025-02-03 14:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('MGPROTOCOLO', '0008_remove_documento_validade_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='processo',
            name='setor_responsavel',
        ),
        migrations.AddField(
            model_name='processo',
            name='setor_atual',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='processos_setoratual', to='MGPROTOCOLO.setor'),
        ),
        migrations.AddField(
            model_name='processo',
            name='setor_fim',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='processos_setorfim', to='MGPROTOCOLO.setor'),
        ),
    ]
