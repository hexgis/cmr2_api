from django.contrib.gis.db import models
from django.utils.translation import ugettext_lazy as _


class LandUseVmRegionalCoordnation(models.Model):
    id = models.IntegerField(
        _('primary key'),
        unique=True,
        primary_key=True,
    )

    cr_co_cr = models.CharField(
        _('Code of Regional Coordination'),
        max_length=255,
        null=True,
        blank=True,
    )

    cr_no_cr = models.CharField(
        _('Name of Regional Coordination'),
        max_length=255,
        null=True,
        blank=True,
    )

    cr_no_regiao = models.CharField(
        _('Regiona Name of Regional Coordination'),
        max_length=255,
        null=True,
        blank=True,
    )

    ti_co_funai = models.CharField(
        _('funai code of Indigenous Land'),
        max_length=255,
        null=True,
        blank=True,
    )

    ti_no_ti = models.CharField(
        _('Name of Indigenous Land'),
        max_length=255,
        null=True,
        blank=True,
    )

    class Meta:
        """Meta class for `models.LandUseTI` model."""
        app_label = 'land_use'
        verbose_name = 'Land Use Mapping Regional Coordination'
        verbose_name_plural = 'Land Use Mapping Regional Coordinations'
        db_table = 'funai\".\"vwm_painel_coordenacao_regional_terra_indigena'
        managed = False


class LandUseClasses(models.Model):
    """LandUseClasses model data for land_use model."""

    id = models.IntegerField(
        _('primary key'),
        unique=True,
        primary_key=True,
    )

    sg_uf = models.CharField(
        _('Brazilian states flag'),
        max_length=255,
        null=True,
        blank=True,
    )

    no_ti = models.CharField(
        _('Name of Indigenous Lands'),
        max_length=255,
        null=True,
        blank=True,
    )

    co_funai = models.IntegerField(
        _('Funai code for Indigenous Land'),
        null=True,
        blank=True,
    )

    dt_homologada = models.CharField(
        _('Date of ratification of Indigenous Lands'),
        max_length=255,
        null=True,
        blank=True,
    )

    ds_cr = models.CharField(
        _('Regional Coordination name'),
        max_length=255,
        null=True,
        blank=True,
    )

    co_cr = models.BigIntegerField(
        _('Regional Coordination code'),
        null=True,
        blank=True,
    )

    nu_ano = models.IntegerField(
        _('Reference mapping year'),
        null=True,
        blank=True,
    )

    no_estagio = models.CharField(
        _('Stage name land use mapping'),
        max_length=255,
        null=True,
        blank=True,
    )

    no_satelites = models.CharField(
        _('Satellites used in mapping'),
        max_length=255,
        null=True,
        blank=True,
    )

    nu_resolucoes = models.CharField(
        _('Satellite spatial resolution'),
        max_length=255,
        null=True,
        blank=True,
    )

    dt_imagens = models.CharField(
        _('Mapped image date'),
        max_length=255,
        null=True,
        blank=True,
    )

    nu_area_km2 = models.DecimalField(
        _('Area polygon km2'),
        max_digits=14,
        decimal_places=3,
        null=True,
        blank=True,
    )

    nu_area_ha = models.DecimalField(
        _('Area polygon ha'),
        max_digits=14,
        decimal_places=3,
        null=True,
        blank=True,
    )

    dt_cadastro = models.CharField(
        _('Registration date'),
        max_length=255,
        null=True,
        blank=True,
    )

    nu_latitude = models.DecimalField(
        _('Latitude'),
        max_digits=20,
        decimal_places=15,
        null=True,
        blank=True,
    )

    nu_longitude = models.DecimalField(
        _('Longitude'),
        max_digits=20,
        decimal_places=15,
        null=True,
        blank=True,
    )

    geom = models.GeometryField(
        _('Geometry Field'),
        srid=4326,
        blank=True,
        null=True,
    )

    class Meta:
        """Meta class for `models.LandUseClasses` model."""
        app_label = 'land_use'
        verbose_name = 'Land Use Mapping Class'
        verbose_name_plural = 'Land Use Mapping Classes'
        db_table = 'funaidados\".\"img_analise_consolidado_oneatlas_dissolvido_por_estagio_a'
        managed = False
