# Generated by Django 4.2.16 on 2025-04-08 21:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('HOME', '0007_modulo_sigla'),
    ]

    operations = [
        migrations.AddField(
            model_name='modulo',
            name='permissao',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='auth.permission'),
        ),
        migrations.CreateModel(
            name='Setor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(blank=True, max_length=255, null=True, unique=True)),
                ('sigla', models.CharField(blank=True, max_length=10, null=True)),
                ('ativo', models.BooleanField(default=True)),
                ('secretaria', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='HOME.secretaria')),
                ('usuarios', models.ManyToManyField(null=True, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Notificacao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=255)),
                ('mensagem', models.TextField()),
                ('lida', models.BooleanField(default=False)),
                ('criada_em', models.DateTimeField(auto_now_add=True)),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
