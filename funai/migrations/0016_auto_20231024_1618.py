# Generated by Django 3.2.3 on 2023-10-24 16:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('funai', '0015_auto_20220613_2107'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='coordenacaoregional',
            options={'verbose_name': 'CoordenacaoRegional', 'verbose_name_plural': 'CoordenacoesRegionais'},
        ),
        migrations.AlterModelOptions(
            name='limiteterraindigena',
            options={'ordering': ('no_ti',), 'verbose_name': 'Indigenous Lands', 'verbose_name_plural': 'Indigenous Lands'},
        ),
    ]
