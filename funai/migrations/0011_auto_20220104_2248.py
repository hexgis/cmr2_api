# Generated by Django 3.2.3 on 2022-01-04 22:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('funai', '0010_remove_coordenacaoregional_co_cr'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='coordenacaoregional',
            name='id',
        ),
        migrations.RemoveField(
            model_name='limiteterraindigena',
            name='co_cr_fk',
        ),
        migrations.AddField(
            model_name='coordenacaoregional',
            name='co_cr',
            field=models.BigIntegerField(default=9999, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AddField(
            model_name='limiteterraindigena',
            name='co_cr',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='CO_CR', to='funai.coordenacaoregional'),
        ),
        migrations.AddField(
            model_name='limiteterraindigena',
            name='nu_area_km',
            field=models.DecimalField(blank=True, decimal_places=10, max_digits=19, null=True),
        ),
        migrations.AlterField(
            model_name='limiteterraindigena',
            name='nu_area_ha',
            field=models.DecimalField(blank=True, decimal_places=10, max_digits=19, null=True),
        ),
    ]