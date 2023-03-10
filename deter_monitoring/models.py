from django.contrib.gis.db import models
from django.utils.translation import ugettext_lazy as _


class DeterTI(models.Model):
    """Model for db view aggregating all satellite scene catalog."""

    classname = models.CharField(
        _('Classification classes'),
        max_length=255,
        null=True,
        blank=True
    )

    quadrant = models.CharField(
        _('Quadrant'),
        max_length=255,
        null=True,
        blank=True
    )

    path_row = models.CharField(
        _('Path and row'),
        max_length=255,
        null=True,
        blank=True
    )

    areatotalkm = models.DecimalField(
        _('Total area km'),
        max_digits=14,
        decimal_places=3,
        blank=True,
        null=True
    )

    areamunkm = models.DecimalField(
        _('City area km'),
        max_digits=14,
        decimal_places=3,
        blank=True,
        null=True
    )

    areauckm = models.DecimalField(
        _('UC area km'),
        max_digits=14,
        decimal_places=3,
        blank=True,
        null=True
    )

    view_date = models.DateField(
        _('Visualization data'),
        null=True,
        blank=True
    )

    sensor = models.CharField(
        _('Optical sensor'),
        max_length=255,
        null=True,
        blank=True
    )

    satellite = models.CharField(
        _('Satellite'),
        max_length=255,
        null=True,
        blank=True
    )

    uf = models.CharField(
        _('State acronym'),
        max_length=255,
        null=True,
        blank=True
    )

    municipality = models.CharField(
        _('City name'),
        max_length=255,
        null=True,
        blank=True
    )

    geocod = models.CharField(
        _('Geo code'),
        max_length=255,
        null=True,
        blank=True
    )

    uc = models.CharField(
        _('Conservation unit'),
        max_length=255,
        null=True,
        blank=True
    )

    publish_month = models.CharField(
        _('Publish month'),
        max_length=255,
        null=True,
        blank=True
    )

    co_cr = models.BigIntegerField(
        _('Regional Coordenation code'),
        blank=True,
        null=True
    )

    ds_cr = models.CharField(
        _('Regional Coordenation name'),
        max_length=255,
        blank=True,
        null=True
    )

    co_funai = models.IntegerField(
        _('Funai code'),
        blank=True,
        null=True
    )

    no_ti = models.CharField(
        _('Name of Indigenous Lands'),
        max_length=255,
        blank=True,
        null=True
    )

    nu_latitude = models.DecimalField(
        _('Latitude'),
        max_digits=20,
        decimal_places=10,
        null=True,
        blank=True
    )

    nu_longitude = models.DecimalField(
        _('Longitude'),
        max_digits=20,
        decimal_places=10,
        null=True,
        blank=True
    )
    geom = models.GeometryField(
        _('Geometry Field'),
        srid=4326,
        blank=True,
        null=True
    )

    class Meta:
        """"Meta class for `deter_monitoring.DeterTI` model."""
        app_label = 'deter_monitoring'
        verbose_name = 'Deter Indigenous Lands'
        verbose_name_plural = 'Deter Indigenous Lands'
        db_table = 'funai\".\"lim_deter_a'
        managed = False
        ordering = ('-view_date', 'no_ti')

    def __str__(self) -> str:
        """Returns `deter_monitoring.DeterTI` string data.

        Returns:
            str: model data name.
        """
        return f'{self.path_row} - {self.view_date} - {self.classname}'
