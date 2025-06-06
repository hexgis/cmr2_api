# Generated by Django 3.2.3 on 2025-02-12 18:47

import django.contrib.gis.db.models.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UrgentAlerts',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False, unique=True, verbose_name='Polygon identifier and primary key')),
                ('no_ciclo', models.CharField(blank=True, max_length=255, null=True, verbose_name='Cycle of monitoring Indigenous Lands in the Legal Amazon')),
                ('no_titulo', models.CharField(blank=True, max_length=255, null=True, verbose_name='Map title - header')),
                ('no_arquivo', models.CharField(blank=True, max_length=255, null=True, verbose_name='Map title - generated in PDF')),
                ('nu_referencia', models.IntegerField(blank=True, null=True, verbose_name='Alert sequential number')),
                ('nu_mapa', models.IntegerField(blank=True, null=True, verbose_name='Map number')),
                ('no_estagio', models.CharField(blank=True, max_length=255, null=True, verbose_name='Stage name')),
                ('no_imagem', models.CharField(blank=True, max_length=255, null=True, verbose_name='Image identifier')),
                ('nu_orbita_ponto', models.CharField(blank=True, max_length=255, null=True, verbose_name='Satellit Sentinel orbit and point')),
                ('dt_t_zero', models.DateField(blank=True, null=True, verbose_name='Data before changes detects')),
                ('dt_t_um', models.DateField(blank=True, null=True, verbose_name='Change start date')),
                ('nu_area_ha', models.DecimalField(blank=True, decimal_places=3, max_digits=14, null=True, verbose_name='Area polygon ha')),
                ('co_funai', models.IntegerField(blank=True, null=True, verbose_name='Funai code - Indigenou Lands')),
                ('no_ti', models.CharField(blank=True, max_length=255, null=True, verbose_name='Indigenou Lands name')),
                ('co_cr', models.BigIntegerField(blank=True, null=True, verbose_name='Regional Coordination code')),
                ('ds_cr', models.CharField(blank=True, max_length=255, null=True, verbose_name='Regional Coordination name')),
                ('no_municipio', models.CharField(blank=True, max_length=255, null=True, verbose_name='City name')),
                ('sg_uf', models.CharField(blank=True, max_length=255, null=True, verbose_name='Abbreviation name')),
                ('nu_latitude', models.DecimalField(blank=True, decimal_places=10, max_digits=20, null=True, verbose_name='Latitude')),
                ('nu_longitude', models.DecimalField(blank=True, decimal_places=10, max_digits=20, null=True, verbose_name='Longitude')),
                ('geom', django.contrib.gis.db.models.fields.GeometryField(blank=True, null=True, srid=4326, verbose_name='Geometry Field')),
            ],
            options={
                'verbose_name': 'Urgent Alert',
                'verbose_name_plural': 'Urgent Alerts',
                'db_table': 'funai"."vw_img_alerta_urgente_consolidado_a',
                'managed': False,
            },
        ),
    ]
