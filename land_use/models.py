from django.contrib.gis.db import models
from django.utils.translation import ugettext_lazy as _


class LandUseMappingTI(models.Model):
    id = models.IntegerField(
        _('primary key'),
        unique=True,
        primary_key=True,
    )
    sg_uf = models.CharField(
        _(''),
        max_length=2,
        null=True,
        blank=True
    )
    no_ti = models.CharField(
        _(''),
        max_length=100,
        null=True,
        blank=True
    )
    co_funai = models.IntegerField(
        _(''),
        null=True,
        blank=True
    )
    dt_homologada = models.CharField(
        _(''),
        max_length=10,
        null=True,
        blank=True
    )
    ds_cr = models.CharField(
        _(''),
        max_length=100,
        null=True,
        blank=True
    )
    nu_ano = models.CharField(
        _(''),
        max_length=4,
        null=True,
        blank=True
    )
    no_satelites = models.CharField(
        _(''),
        max_length=50,
        null=True,
        blank=True
    )
    nu_resolucoes = models.CharField(
        _(''),
        max_length=50,
        null=True,
        blank=True
    )
    dt_imagens = models.CharField(
        _(''),
        max_length=10,
        null=True,
        blank=True
    )
    nu_area_ag_ha = models.FloatField(
        _(''),
        null=True,
        blank=True,
    )
    nu_area_cr_ha = models.FloatField(
        _(''),
        null=True,
        blank=True,
    )
    nu_area_dg_ha = models.FloatField(
        _(''),
        null=True,
        blank=True,
    )
    nu_area_ma_ha = models.FloatField(
        _(''),
        null=True,
        blank=True,
    )
    nu_area_no_ha = models.FloatField(
        _(''),
        null=True,
        blank=True,
    )
    nu_area_rv_ha = models.FloatField(
        _(''),
        null=True,
        blank=True,
    )
    nu_area_sv_ha = models.FloatField(
        _(''),
        null=True,
        blank=True,
    )
    nu_area_vi_ha = models.FloatField(
        _(''),
        null=True,
        blank=True,
    )
    nu_area_vn_ha = models.FloatField(
        _(''),
        null=True,
        blank=True,
    )
    nu_area_mi_ha = models.FloatField(
        _(''),
        null=True,
        blank=True,
    )
    nu_area_ha = models.FloatField(
        _(''),
        null=True,
        blank=True,
    )
    nu_area_km2 = models.FloatField(
        _(''),
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
        app_label = 'land_use'
        verbose_name = 'Land Use Mapping TI'
        verbose_name_plural = 'Land Use Mapping TIs'
        # db_table = 'funaidados\".\"img_analise_consolidado_oneatlas_dissolvido_por_ti_a'
        # managed = False


class LandUseMappingClasses(models.Model):
    id = models.IntegerField(
        _('primary key'),
        unique=True,
        primary_key=True,
    ),
    sg_uf = models.CharField(
        _(''),
        max_length=2,
        null=True,
        blank=True
    )
    no_ti = models.CharField(
        _(''),
        max_length=100,
        null=True,
        blank=True
    )
    co_funai = models.IntegerField(
        _(''),
        null=True,
        blank=True
    )
    dt_homologada = models.CharField(
        _(''),
        max_length=10,
        null=True,
        blank=True
    )
    ds_cr = models.CharField(
        _(''),
        max_length=100,
        null=True,
        blank=True
    )
    nu_ano = models.CharField(
        _(''),
        max_length=4,
        null=True,
        blank=True
    )
    no_estagio = models.CharField(
        _(''),
        max_length=2,
        null=True,
        blank=True
    )
    no_satelites = models.CharField(
        _(''),
        max_length=50,
        null=True,
        blank=True
    )
    nu_resolucoes = models.CharField(
        _(''),
        max_length=50,
        null=True,
        blank=True
    )
    dt_imagens = models.CharField(
        _(''),
        max_length=10,
        null=True,
        blank=True
    )
    nu_area_ha = models.FloatField(
        _(''),
        null=True,
        blank=True,
    )
    # Remover, esse não está no CMR1
    nu_area_ha = models.FloatField(
        _(''),
        null=True,
        blank=True,
    )
    # Remover, esse não está no CMR1
    dt_cadastro = models.DateField(
        _('Date of'),
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
        app_label = 'land_use'
        verbose_name = 'Land Use Mapping Class'
        verbose_name_plural = 'Land Use Mapping Classes'
        # db_table = 'funaidados\".\"img_analise_consolidado_oneatlas_dissolvido_por_estagio_a'
        # managed = False
