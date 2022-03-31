from django.contrib.gis.db import models
from django.utils.translation import ugettext_lazy as _


class PriorityConsolidated(models.Model):
    """PriorityConsolidated model data for priority_monitoring model."""

    id = models.IntegerField(
        _('Identifier and primary key'),
        unique=True,
        primary_key=True,
    )

    tb_ciclo_monitoramento_id = models.IntegerField(
        _('Monitoring cycle identifier'),
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

    dt_imagem = models.DateField(
        _('Image date'),
        null=True,
        blank=True,
    )

    nu_orbita = models.CharField(
        _('Path number'),
        max_length=255,
        null=True,
        blank=True,
    )

    nu_ponto = models.CharField(
        _('Row number'),
        max_length=255,
        null=True,
        blank=True,
    )

    dt_t_zero = models.DateField(
        _('Date of first detected change'),
        null=True,
        blank=True,
    )

    dt_t_um = models.DateField(
        _('Date of changes hadn"t began'),
        null=True,
        blank=True,
    )

    nu_area_km2 = models.DecimalField(
        _('Area km'),
        max_digits=20,
        decimal_places=15,
        null=True,
        blank=True,
    )

    nu_area_ha = models.DecimalField(
        _('Area ha'),
        max_digits=20,
        decimal_places=15,
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

    tempo = models.IntegerField(
        _('Time'),
        null=True,
        blank=True,
    )

    contribuicao = models.IntegerField(
        _('Contribution'),
        null=True,
        blank=True,
    )

    velocidade = models.DecimalField(
        _('Speed'),
        max_digits=20,
        decimal_places=15,
        null=True,
        blank=True,
    )

    contiguidade = models.IntegerField(
        _('Contiguity'),
        null=True,
        blank=True,
    )

    ranking = models.DecimalField(
        _('Ranking'),
        max_digits=20,
        decimal_places=15,
        null=True,
        blank=True,
    )

    prioridade = models.CharField(
        _('Priority'),
        max_length=255,
        null=True,
        blank=True,
    )

    dt_cadastro = models.DateTimeField(
        _('Register Date'),
        null=True,
        blank=True,
    )

    co_cr = models.BigIntegerField(
        _('Regional Coordenation code'),
        default=1,
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
        default=1,
        blank=True,
        null=True,
    )

    no_ti = models.CharField(
        _('Indigenou Lands name'),
        max_length=255,
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
        """Meta class for `priority_monitoring.PriorityConsolidated` model."""
        app_label = 'priority_monitoring'
        verbose_name = 'Priority Consolidated'
        verbose_name_plural = 'Prioritys Consolidated'
        ordering = ('-dt_t_zero', 'ranking', 'no_estagio')
        db_table = 'funaidados\".\"vwm_monitoramento_consolidado_priorizacao_a'
        managed = False

    def __str__(self):
        """Returns `priority_monitoring.PriorityConsolidated` string data.

        Returns:
            str: model data name.
        """
        return f'{self.dt_t_zero} - {self.dt_t_um}'
