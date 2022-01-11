from django.contrib.gis.db import models
from django.utils.translation import ugettext_lazy as _
from django.db.models.fields import BooleanField


class PriorityConsolidated(models.Model):
    """PriorityConsolidated model data for priority model."""

    id_tb = models.IntegerField(
        _('Table identifier'),
        null=True,
        blank=True,
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

    no_image = models.CharField(
        _('Image identifier'),
        max_length=255,
        null=True,
        blank=True,
    )

    dt_image = models.DateField(
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

    dt_t0 = models.DateField(
        _('Date of first detected change'),
        null=True,
        blank=True,
    )

    dt_t1 = models.DateField(
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

    geom = models.GeometryField(
        _('Geometry Field'),
        srid=4326,
        blank=True,
        null=True,
    )

    no_cr = models.CharField(
        _('Regional Coordination name'),
        max_length=255,
        null=True,
        blank=True,
    )

    no_ti = models.CharField(
        _('Indigenou Lands name'),
        max_length=255,
        null=True,
        blank=True,
    )

    flag = models.BooleanField(
        _('Flag'),
        default=False
    )

    class Meta:
        app_label = 'priority_monitoring'
        verbose_name = 'PriorityConsolidated'
        verbose_name_plural = 'PrioritysConsolidated'
        ordering = ["-dt_t0", "ranking", "no_estagio"]

    def __str__(self):
        """Returns a string class based name.

        Returns:
            str: model data named.
        """
        return f'{self.dt_t0} - {self.dt_t1}'
