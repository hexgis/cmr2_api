# Generated by Django 3.2.3 on 2024-08-01 13:06

import django.contrib.gis.db.models.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PriorityConsolidated',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False, unique=True, verbose_name='Identifier and primary key')),
                ('tb_ciclo_monitoramento_id', models.IntegerField(blank=True, null=True, verbose_name='Monitoring cycle identifier')),
                ('no_estagio', models.CharField(blank=True, max_length=255, null=True, verbose_name='Stage name')),
                ('no_imagem', models.CharField(blank=True, max_length=255, null=True, verbose_name='Image identifier')),
                ('dt_imagem', models.DateField(blank=True, null=True, verbose_name='Image date')),
                ('nu_orbita', models.CharField(blank=True, max_length=255, null=True, verbose_name='Path number')),
                ('nu_ponto', models.CharField(blank=True, max_length=255, null=True, verbose_name='Row number')),
                ('dt_t_zero', models.DateField(blank=True, null=True, verbose_name='Date of first detected change')),
                ('dt_t_um', models.DateField(blank=True, null=True, verbose_name='Date of changes hadn"t began')),
                ('nu_area_km2', models.DecimalField(blank=True, decimal_places=3, max_digits=14, null=True, verbose_name='Area km')),
                ('nu_area_ha', models.DecimalField(blank=True, decimal_places=3, max_digits=14, null=True, verbose_name='Area ha')),
                ('nu_latitude', models.DecimalField(blank=True, decimal_places=10, max_digits=20, null=True, verbose_name='Latitude')),
                ('nu_longitude', models.DecimalField(blank=True, decimal_places=10, max_digits=20, null=True, verbose_name='Longitude')),
                ('tempo', models.IntegerField(blank=True, null=True, verbose_name='Time')),
                ('contribuicao', models.IntegerField(blank=True, null=True, verbose_name='Contribution')),
                ('velocidade', models.DecimalField(blank=True, decimal_places=10, max_digits=20, null=True, verbose_name='Speed')),
                ('contiguidade', models.IntegerField(blank=True, null=True, verbose_name='Contiguity')),
                ('ranking', models.DecimalField(blank=True, decimal_places=10, max_digits=20, null=True, verbose_name='Ranking')),
                ('prioridade', models.CharField(blank=True, max_length=255, null=True, verbose_name='Priority')),
                ('dt_cadastro', models.DateTimeField(blank=True, null=True, verbose_name='Register Date')),
                ('co_cr', models.BigIntegerField(blank=True, default=1, null=True, verbose_name='Regional Coordenation code')),
                ('ds_cr', models.CharField(blank=True, max_length=255, null=True, verbose_name='Regional Coordination name')),
                ('co_funai', models.IntegerField(blank=True, default=1, null=True, verbose_name='Funai code - Indigenou Lands')),
                ('no_ti', models.CharField(blank=True, max_length=255, null=True, verbose_name='Indigenou Lands name')),
                ('geom', django.contrib.gis.db.models.fields.GeometryField(blank=True, null=True, srid=4326, verbose_name='Geometry Field')),
            ],
            options={
                'verbose_name': 'Priority Consolidated',
                'verbose_name_plural': 'Priorities Consolidated',
                'db_table': 'funaidados"."vwm_monitoramento_consolidado_priorizacao_a',
                'ordering': ('-ranking', 'no_estagio'),
                'managed': False,
            },
        ),
    ]
