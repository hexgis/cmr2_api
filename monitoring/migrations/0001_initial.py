# Generated by Django 3.2.3 on 2024-08-01 13:06

import django.contrib.gis.db.models.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MonitoringConsolidated',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False, unique=True, verbose_name='Polygon identifier and primary key')),
                ('no_imagem', models.CharField(blank=True, max_length=255, null=True, verbose_name='Image identifier')),
                ('dt_cadastro', models.DateField(blank=True, null=True, verbose_name='Date of registration')),
                ('dt_imagem', models.DateField(blank=True, null=True, verbose_name='Image date')),
                ('no_estagio', models.CharField(blank=True, max_length=255, null=True, verbose_name='Stage name')),
                ('dt_t_zero', models.DateField(blank=True, null=True, verbose_name='Data before changes detects')),
                ('dt_t_um', models.DateField(blank=True, null=True, verbose_name='Date of changes hadn"t began')),
                ('nu_area_km2', models.DecimalField(blank=True, decimal_places=3, max_digits=14, null=True, verbose_name='Area polygon km2')),
                ('nu_area_ha', models.DecimalField(blank=True, decimal_places=3, max_digits=14, null=True, verbose_name='Area polygon ha')),
                ('no_ciclo', models.CharField(blank=True, max_length=255, null=True, verbose_name='Cycle of monitoring Indigenous Lands in the Legal Amazon')),
                ('nu_orbita', models.CharField(blank=True, max_length=255, null=True, verbose_name='Satellit Sentinel orbit')),
                ('nu_ponto', models.CharField(blank=True, max_length=255, null=True, verbose_name='Orbit point')),
                ('nu_latitude', models.DecimalField(blank=True, decimal_places=10, max_digits=20, null=True, verbose_name='Latitude')),
                ('nu_longitude', models.DecimalField(blank=True, decimal_places=10, max_digits=20, null=True, verbose_name='Longitude')),
                ('co_cr', models.BigIntegerField(blank=True, null=True, verbose_name='Funai code')),
                ('ds_cr', models.CharField(blank=True, max_length=255, null=True, verbose_name='Regional Coordination name')),
                ('co_funai', models.IntegerField(blank=True, null=True, verbose_name='Funai code - Indigenou Lands')),
                ('no_ti', models.CharField(blank=True, max_length=255, null=True, verbose_name='Indigenou Lands name')),
                ('ti_nu_area_ha', models.DecimalField(blank=True, decimal_places=3, max_digits=14, null=True, verbose_name='Area Indigenou Lands ha')),
                ('geom', django.contrib.gis.db.models.fields.GeometryField(blank=True, null=True, srid=4326, verbose_name='Geometry Field')),
            ],
            options={
                'verbose_name': 'Monitoring Consolidated',
                'verbose_name_plural': 'Monitorings Consolidated',
                'db_table': 'funaidados"."img_monitoramento_terra_indigena_cr_a',
                'ordering': ('-dt_t_um',),
                'managed': False,
            },
        ),
    ]
