# Generated by Django 4.2.16 on 2024-11-28 19:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='veiculo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('placa', models.CharField(max_length=8)),
                ('secretaria', models.CharField(max_length=50)),
                ('modelo', models.CharField(max_length=100, null=True)),
                ('descricao', models.TextField(null=True)),
                ('observacao', models.TextField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='fiscal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='condutor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Abastecimentos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.DateField()),
                ('tipo', models.CharField(max_length=30)),
                ('quantidade', models.FloatField()),
                ('valorUnitario', models.FloatField()),
                ('valorTotal', models.FloatField()),
                ('km', models.IntegerField()),
                ('status', models.CharField(max_length=10)),
                ('condutor', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='MGCOMBUSTIVEIS.condutor')),
                ('fiscal', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='MGCOMBUSTIVEIS.fiscal')),
                ('placa', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='MGCOMBUSTIVEIS.veiculo')),
            ],
        ),
    ]