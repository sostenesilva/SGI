# Generated by Django 4.2.16 on 2025-02-27 18:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MGTRANSPARENCIA', '0003_dbavaliacao_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dbcriterios',
            name='classificacao',
            field=models.CharField(choices=[('Obrigatória', 'Obrigatória'), ('Essencial', 'Essencial'), ('Recomendada', 'Recomendada')], default='Obrigatório', max_length=20, verbose_name='Classificação'),
        ),
        migrations.AlterField(
            model_name='dbcriterios',
            name='item',
            field=models.CharField(max_length=6, verbose_name='Código do Item'),
        ),
    ]
