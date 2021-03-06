# Generated by Django 3.2.3 on 2022-06-13 21:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('funai', '0014_auto_20220307_1334'),
    ]

    operations = [
        migrations.AlterField(
            model_name='limiteterraindigena',
            name='nu_area_ha',
            field=models.DecimalField(blank=True, decimal_places=3, max_digits=14, null=True, verbose_name='Area ha'),
        ),
        migrations.AlterField(
            model_name='limiteterraindigena',
            name='nu_area_km',
            field=models.DecimalField(blank=True, decimal_places=3, max_digits=14, null=True, verbose_name='Area km'),
        ),
    ]
