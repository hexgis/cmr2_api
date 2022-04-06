from funai.models import CoordenacaoRegional, LimiteTerraIndigena

from django.contrib.gis.db import models
from django.utils.translation import ugettext_lazy as _


class MonitoringConsolidated(models.Model):
    """MonitoringConsolidated model data for monitoring model."""

    id = models.IntegerField(
        _('Polygon identifier and primary key'),
        unique=True,
        primary_key=True,
    )

    tb_ciclo_monitoramento_id = models.IntegerField(
        _('Monitoring cycle identifier'),
        null=True,
        blank=True,
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

    dt_cadastro = models.DateField(
        _('Date of register polygon change'),
        null=True,
        blank=True,
    )

    dt_t_um = models.DateField(
        _('Date of changes hadn"t began'),
        null=True,
        blank=True,
    )

    nu_area_km2 = models.BigIntegerField(
        _('Area polygon km2'),
        null=True,
        blank=True,
    )

    nu_area_ha = models.BigIntegerField(
        _('Area polygon ha'),
        null=True,
        blank=True,
    )

    co_cr = models.ForeignKey(
        CoordenacaoRegional,
        blank=True,
        null=True,
        to_field='co_cr',
        related_name='cr_monitoring',
        on_delete=models.DO_NOTHING,
    )

    ds_cr = models.CharField(
        _('Regional Coordination name'),
        max_length=255,
        null=True,
        blank=True,
    )

    co_funai = models.ForeignKey(
        LimiteTerraIndigena,
        blank=True,
        null=True,
        to_field='co_funai',
        related_name='ti_monitoring',
        on_delete=models.DO_NOTHING,
    )

    no_ti = models.CharField(
        _('Indigenou Lands name'),
        max_length=255,
        null=True,
        blank=True,
    )

    ti_nu_area_ha = models.BigIntegerField(
        _('Area Indigenou Lands ha'),
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

    def __str__(self) -> str:
        """Returns `monitoring.Monitoring.Consolidated` string data.

        Returns:
            str: model data name.
        """
        return f'{self.no_ti} - {self.dt_t_um} - {self.no_estagio}'
