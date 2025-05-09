# Generated by Django 4.2.16 on 2025-01-30 19:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('MGPROTOCOLO', '0006_processo_rename_data_criacao_documento_criado_em_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='documento',
            name='ativo',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='documento',
            name='tipo',
            field=models.CharField(blank=True, choices=[('inicial', 'Documento Inicial'), ('complementar', 'Documento Complementar')], default='inicial', max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='documento',
            name='validade',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='movimentacao',
            name='ativo',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='movimentacao',
            name='observacoes',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='movimentacao',
            name='setor_origem',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='movimentacoes_origem', to='MGPROTOCOLO.setor'),
        ),
        migrations.AddField(
            model_name='processo',
            name='ativo',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='processo',
            name='prazo',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='processo',
            name='status',
            field=models.CharField(blank=True, choices=[('em_analise', 'Em análise'), ('concluido', 'Concluído'), ('cancelado', 'Cancelado')], default='em_analise', max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='processo',
            name='ultima_movimentacao',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='processo_ultima_movimentacao', to='MGPROTOCOLO.movimentacao'),
        ),
        migrations.AddField(
            model_name='setor',
            name='ativo',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='setor',
            name='sigla',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='documento',
            name='classificacao',
            field=models.CharField(blank=True, choices=[('oficio', 'Ofício'), ('ci', 'Comunicado Interno'), ('memorando', 'Memorando'), ('parecer', 'Parecer'), ('laudo', 'Láudo'), ('relatorio', 'Relatório'), ('contrato', 'Contrato'), ('edital', 'Edital'), ('cotacoes', 'Cotações'), ('outros', 'Outros')], max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='movimentacao',
            name='confirmado_por',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='movimentacoes_confirmadas', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='movimentacao',
            name='realizado_em',
            field=models.DateTimeField(auto_now_add=True, db_index=True, null=True),
        ),
        migrations.AlterField(
            model_name='movimentacao',
            name='realizado_por',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='movimentacao',
            name='setor_destino',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='movimentacoes_destino', to='MGPROTOCOLO.setor'),
        ),
        migrations.AlterField(
            model_name='processo',
            name='numero',
            field=models.CharField(blank=True, db_index=True, max_length=20, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='processo',
            name='setor_demandante',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='processos_demandantes', to='MGPROTOCOLO.setor'),
        ),
        migrations.AlterField(
            model_name='processo',
            name='setor_responsavel',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='processos_responsaveis', to='MGPROTOCOLO.setor'),
        ),
    ]
