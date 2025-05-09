# Generated by Django 4.2.16 on 2025-02-12 18:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MGPROTOCOLO', '0009_remove_processo_setor_responsavel_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movimentacao',
            name='status',
            field=models.CharField(blank=True, choices=[('em_tramitacao', 'Em tramitação'), ('recebida', 'Recebida'), ('arquivada', 'Arquivada')], default='em_tramitacao', max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='processo',
            name='numero',
            field=models.CharField(blank=True, db_index=True, max_length=100, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='processo',
            name='status',
            field=models.CharField(blank=True, choices=[('em_analise', 'Em análise'), ('concluido', 'Concluído'), ('cancelado', 'Cancelado'), ('arquivado', 'Arquivado')], default='em_analise', max_length=20, null=True),
        ),
    ]
