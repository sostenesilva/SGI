# Generated by Django 4.2.16 on 2025-01-08 13:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MGREGULARIDADEFISCAL', '0002_certidao_irregular'),
    ]

    operations = [
        migrations.AddField(
            model_name='declaracao',
            name='arquivo',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
        migrations.AddField(
            model_name='declaracao',
            name='data_inicio',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='declaracao',
            name='data_validade',
            field=models.DateField(blank=True, null=True),
        ),
    ]
