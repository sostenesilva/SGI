# Generated by Django 4.2.16 on 2025-05-14 19:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MGC', '0007_saidasec_saldocontratosec'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ordem',
            old_name='dataehora',
            new_name='dataregistro',
        ),
        migrations.AddField(
            model_name='ordem',
            name='dataemissao',
            field=models.DateField(blank=True, null=True),
        ),
    ]
