# Generated by Django 4.2.16 on 2025-02-28 17:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('MGTRANSPARENCIA', '0008_alter_dbcriterios_periodicidade'),
    ]

    operations = [
        migrations.RenameField(
            model_name='informacoescriterio',
            old_name='documentos',
            new_name='documento',
        ),
    ]
