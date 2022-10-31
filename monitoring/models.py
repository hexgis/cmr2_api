from django.contrib.gis.db import models
from django.utils.translation import ugettext_lazy as _


class MonitoringConsolidated(models.Model):
    """MonitoringConsolidated model data for monitoring model."""

    id = models.IntegerField(
        _('Polygon identifier and primary key'),
        unique=True,
        primary_key=True,
    )

    no_imagem = models.CharField(
        _('Image identifier'),
        max_length=255,
        null=True,
        blank=True,
    )

    dt_imagem = models.DateField(
        _('Image date'),
        null=True,
        blank=True,
    )

    no_estagio = models.CharField(
        _('Stage name'),
        max_length=255,
        null=True,
        blank=True,
    )

    dt_t_zero = models.DateField(
        _('Data before changes detects'),
        null=True,
        blank=True,
    )

    dt_t_um = models.DateField(
        _('Date of changes hadn"t began'),
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

    no_ciclo = models.CharField(
        _('Cycle of monitoring Indigenous Lands in the Legal Amazon'),
        max_length=255,
        null=True,
        blank=True,
    )

    nu_orbita = models.CharField(
        _('Satellit Sentinel orbit'),
        max_length=255,
        null=True,
        blank=True,
    )

    nu_ponto = models.CharField(
        _('Orbit point'),
        max_length=255,
        null=True,
        blank=True,
    )

    nu_latitude = models.DecimalField(
        _('Latitude'),
        max_digits=20,
        decimal_places=10,
        null=True,
        blank=True,
    )

    nu_longitude = models.DecimalField(
        _('Longitude'),
        max_digits=20,
        decimal_places=10,
        null=True,
        blank=True,
    )

    co_cr = models.BigIntegerField(
        _('Funai code'),
        blank=True,
        null=True,
    )

    ds_cr = models.CharField(
        _('Regional Coordination name'),
        max_length=255,
        null=True,
        blank=True,
    )

    co_funai = models.IntegerField(
        _('Funai code - Indigenou Lands'),
        blank=True,
        null=True,
    )

    no_ti = models.CharField(
        _('Indigenou Lands name'),
        max_length=255,
        null=True,
        blank=True,
    )

    ti_nu_area_ha = models.DecimalField(
        _('Area Indigenou Lands ha'),
        max_digits=14,
        decimal_places=3,
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
        """Meta class for `monitoring.MonitoringConsolidated` model."""
        app_label = 'monitoring'
        verbose_name = 'Monitoring Consolidated'
        verbose_name_plural = 'Monitorings Consolidated'
        ordering = ('-dt_t_um',)
        db_table = 'funaidados\".\"img_monitoramento_terra_indigena_cr_a'
        managed = False

    def __str__(self) -> str:
        """Returns `monitoring.Monitoring.Consolidated` string data.

        Returns:
            str: model data name.
        """
        return f'{self.no_ti} - {self.dt_t_um} - {self.no_estagio}'


class MonitoringConsolidatedStats(models.Model):
    """MonitoringConsolidated model data for monitoring model."""

    no_imagem = models.CharField(
        _('Image identifier'),
        max_length=255,
        null=True,
        blank=True,
    )

    dt_imagem = models.DateField(
        _('Image date'),
        null=True,
        blank=True,
    )

    no_estagio = models.CharField(
        _('Stage name'),
        max_length=255,
        null=True,
        blank=True,
    )

    dt_t_um = models.DateField(
        _('Date of changes hadn"t began'),
        null=True,
        blank=True,
    )

    dt_cadastro = models.DateField(
        _('Date of registration'),
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

    no_ciclo = models.CharField(
        _('Cycle of monitoring Indigenous Lands in the Legal Amazon'),
        max_length=255,
        null=True,
        blank=True,
    )

    co_cr = models.BigIntegerField(
        _('Funai code'),
        blank=True,
        null=True,
    )

    ds_cr = models.CharField(
        _('Regional Coordination name'),
        max_length=255,
        null=True,
        blank=True,
    )

    co_funai = models.IntegerField(
        _('Funai code - Indigenou Lands'),
        blank=True,
        null=True,
    )

    no_ti = models.CharField(
        _('Indigenou Lands name'),
        max_length=255,
        null=True,
        blank=True,
    )

    ti_nu_area_ha = models.DecimalField(
        _('Area Indigenou Lands ha'),
        max_digits=14,
        decimal_places=3,
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
        app_label = 'monitoring'
        verbose_name = 'Monitoring Consolidated Statistic'
        verbose_name_plural = 'Monitorings Consolidated Statistics'
        # db_table = 'funaidados\".\"img_monitoramento_ti_consolidado_a'
        # managed = False
