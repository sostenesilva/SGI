# Generated by Django 4.2.16 on 2025-01-06 20:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MGREGULARIDADEFISCAL', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='certidao',
            name='irregular',
            field=models.BooleanField(default=False),
        ),
    ]
