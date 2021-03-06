# Generated by Django 3.2.3 on 2022-01-11 20:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('funai', '0012_alter_coordenacaoregional_co_cr'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='coordenacaoregional',
            options={'ordering': ('no_cr',), 'verbose_name': 'CoordenacaoRegional', 'verbose_name_plural': 'CoordenacoesRegionais'},
        ),
        migrations.AlterModelOptions(
            name='limiteterraindigena',
            options={'ordering': ('-no_ti',), 'verbose_name': 'Indigenous Lands', 'verbose_name_plural': 'Indigenous Lands'},
        ),
        migrations.AlterField(
            model_name='coordenacaoregional',
            name='co_cr',
            field=models.BigIntegerField(default=1, primary_key=True, serialize=False, unique=True, verbose_name='Regional Coordenation code'),
        ),
        migrations.AlterField(
            model_name='coordenacaoregional',
            name='ds_email',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Email'),
        ),
        migrations.AlterField(
            model_name='coordenacaoregional',
            name='ds_telefone',
            field=models.CharField(blank=True, max_length=512, null=True, verbose_name='Contact number'),
        ),
        migrations.AlterField(
            model_name='coordenacaoregional',
            name='dt_cadastro',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Register date'),
        ),
        migrations.AlterField(
            model_name='coordenacaoregional',
            name='no_abreviado',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Regional Coordenation acronym'),
        ),
        migrations.AlterField(
            model_name='coordenacaoregional',
            name='no_cr',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Regional Coordenation name'),
        ),
        migrations.AlterField(
            model_name='coordenacaoregional',
            name='no_municipio',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='City name'),
        ),
        migrations.AlterField(
            model_name='coordenacaoregional',
            name='no_regiao',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Region name'),
        ),
        migrations.AlterField(
            model_name='coordenacaoregional',
            name='no_uf',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='State'),
        ),
        migrations.AlterField(
            model_name='coordenacaoregional',
            name='sg_cr',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Regional Coordenation flag'),
        ),
        migrations.AlterField(
            model_name='coordenacaoregional',
            name='sg_uf',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='State acronym'),
        ),
        migrations.AlterField(
            model_name='coordenacaoregional',
            name='st_situacao',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Situation'),
        ),
        migrations.AlterField(
            model_name='limiteterraindigena',
            name='co_cr',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='cr', to='funai.coordenacaoregional'),
        ),
        migrations.AlterField(
            model_name='limiteterraindigena',
            name='co_funai',
            field=models.IntegerField(blank=True, null=True, unique=True, verbose_name='Funai code'),
        ),
        migrations.AlterField(
            model_name='limiteterraindigena',
            name='ds_cr',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Description for Regional Coordination'),
        ),
        migrations.AlterField(
            model_name='limiteterraindigena',
            name='ds_fase_ti',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Description for TI stage'),
        ),
        migrations.AlterField(
            model_name='limiteterraindigena',
            name='ds_modalidade',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Modality'),
        ),
        migrations.AlterField(
            model_name='limiteterraindigena',
            name='no_ti',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Name of Indigenous Lands'),
        ),
        migrations.AlterField(
            model_name='limiteterraindigena',
            name='nu_area_ha',
            field=models.DecimalField(blank=True, decimal_places=10, max_digits=19, null=True, verbose_name='Area ha'),
        ),
        migrations.AlterField(
            model_name='limiteterraindigena',
            name='nu_area_km',
            field=models.DecimalField(blank=True, decimal_places=10, max_digits=19, null=True, verbose_name='Area km'),
        ),
        migrations.AlterField(
            model_name='limiteterraindigena',
            name='sg_uf',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='State aconymn'),
        ),
        migrations.AlterField(
            model_name='limiteterraindigena',
            name='st_faixa_fronteira',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Border strip'),
        ),
    ]
