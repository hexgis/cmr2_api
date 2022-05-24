from django.contrib.gis.db import models
from django.utils.translation import ugettext_lazy as _


class LandUseTI(models.Model):
    """LandUseTI model data for land_use model."""

    id = models.IntegerField(
        _('primary key'),
        unique=True,
        primary_key=True,
    )

    sg_uf = models.CharField(
        _('Brazilian states flag'),
        max_length=255,
        null=True,
        blank=True
    )

    no_ti = models.CharField(
        _('Name of Indigenous Lands'),
        max_length=255,
        null=True,
        blank=True
    )

    co_funai = models.IntegerField(
        _('Funai code for Indigenous Lands'),
        null=True,
        blank=True
    )

    dt_homologada = models.CharField(
        _('Date of ratification of Indigenous Lands'),
        max_length=255,
        null=True,
        blank=True
    )

    ds_cr = models.CharField(
        _('Regional Coordination name'),
        max_length=255,
        null=True,
        blank=True
    )

    co_cr = models.BigIntegerField(
        _('Regional Coordination code'),
        null=True,
        blank=True
    )

    nu_ano = models.IntegerField(
        _('Reference mapping year'),
        null=True,
        blank=True
    )

    no_satelites = models.CharField(
        _('Satellites used in mapping'),
        max_length=255,
        null=True,
        blank=True
    )

    nu_resolucoes = models.CharField(
        _('Satellite spatial resolution'),
        max_length=255,
        null=True,
        blank=True
    )

    dt_imagens = models.CharField(
        _('Mapped image date'),
        max_length=255,
        null=True,
        blank=True
    )

    nu_area_ag_ha = models.FloatField(
        _('Area agricultural polygon ha'),
        null=True,
        blank=True,
    )

    nu_area_cr_ha = models.FloatField(
        _('Area clear cut polygon ha'),
        null=True,
        blank=True,
    )

    nu_area_dg_ha = models.FloatField(
        _('Area degradation polygon ha'),
        null=True,
        blank=True,
    )

    nu_area_ma_ha = models.FloatField(
        _('Area body of water polygon ha'),
        null=True,
        blank=True,
    )

    nu_area_no_ha = models.FloatField(
        _('Area not observed polygon ha'),
        null=True,
        blank=True,
    )

    nu_area_rv_ha = models.FloatField(
        _('Area highway polygon ha'),
        null=True,
        blank=True,
    )

    nu_area_sv_ha = models.FloatField(
        _('Area forestry polygon ha'),
        null=True,
        blank=True,
    )

    nu_area_vi_ha = models.FloatField(
        _('Area village polygon ha'),
        null=True,
        blank=True,
    )

    nu_area_vn_ha = models.FloatField(
        _('Area natural vegetation polygon ha'),
        null=True,
        blank=True,
    )

    nu_area_mi_ha = models.FloatField(
        _('Area mining polygon ha'),
        null=True,
        blank=True,
    )

    nu_area_ha = models.FloatField(
        _('Area polygon ha'),
        null=True,
        blank=True,
    )

    nu_area_km2 = models.FloatField(
        _('Area polygon km2'),
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
        null=True,
        blank=True,
    )

    class Meta:
        """Meta class for `models.LandUseTI` model."""
        app_label = 'land_use'
        verbose_name = 'Land Use Mapping TI'
        verbose_name_plural = 'Land Use Mapping TIs'
        db_table = 'funaidados\".\"img_analise_consolidado_oneatlas_dissolvido_por_ti_a'
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

    nu_area_km2 = models.FloatField(
        _('Area polygon km2'),
        null=True,
        blank=True,
    )

    nu_area_ha = models.FloatField(
        _('Area polygon ha'),
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
