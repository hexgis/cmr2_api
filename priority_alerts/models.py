from django.contrib.gis.db import models

from django.utils.translation import ugettext_lazy as _


class UrgentAlerts(models.Model):
    """UrgentAlerts model data for priority_alerts."""

    id = models.IntegerField(
        _('Polygon identifier and primary key'),
        unique=True,
        primary_key=True,
    )

    no_ciclo = models.CharField(
        _('Cycle of monitoring Indigenous Lands in the Legal Amazon'),
        max_length=255,
        null=True,
        blank=True,
    )

    no_titulo = models.CharField(
        _('Map title - header'),
        max_length=255,
        null=True,
        blank=True,
    )

    no_arquivo = models.CharField(
        _('Map title - generated in PDF'),
        max_length=255,
        null=True,
        blank=True,
    )

    nu_referencia = models.IntegerField(
        _('Alert sequential number'),
        null=True,
        blank=True,
    )

    nu_mapa = models.IntegerField(
        _('Map number'),
        null=True,
        blank=True,
    )

    no_estagio = models.CharField(
        _('Stage name'),
        max_length=255,
        null=True,
        blank=True,
    )

    no_imagem = models.CharField(
        _('Image identifier'),
        max_length=255,
        null=True,
        blank=True,
    )

    nu_orbita_ponto = models.CharField(
        _('Satellit Sentinel orbit and point'),
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
        _('Change start date'),
        null=True,
        blank=True,
    )

    nu_area_ha = models.DecimalField(
        _('Area polygon ha'),
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
    )

    co_funai = models.IntegerField(
        _('Funai code - Indigenou Lands'),
        null=True,
        blank=True,
    )

    no_ti = models.CharField(
        _('Indigenou Lands name'),
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

    no_municipio = models.CharField(
        _('City name'),
        max_length=255,
        null=True,
        blank=True,
    )

    sg_uf = models.CharField(
        _('Abbreviation name'),
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
        null=True,
        blank=True,
    )

    class Meta:
        """Meta class for `models.UrgentAlerts` model."""
        app_label = 'priority_alerts'
        verbose_name = 'Urgent Alert'
        verbose_name_plural = 'Urgent Alerts'
        # db_table = 'funai\".\"vw_img_alerta_urgente_consolidado_a'
        # managed = False
