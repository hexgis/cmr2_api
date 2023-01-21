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
        #???
        max_length=255,
        blank=True
    )

    path_row = models.CharField(
        _('Path row'),
        max_length=255,
        null=True,
        blank=True
    )

    areatotalkm = models.DecimalField(
        _('Total area km'),
        #???
        max_digits=14,
        decimal_places=3,
        blank=True,
        null=True
    )

    areamunkm = models.DecimalField(
        _('Mu area km'),
        #???
        max_digits=14,
        decimal_places=3,
        blank=True,
        null=True
    )

    areauckm = models.DecimalField(
        _('uk area km'),
        #???
        max_digits=14,
        decimal_places=3,
        blank=True,
        null=True
    )

    view_date = models.DateField(
        _('Visualization data'),
        #???
        null=True,
        blank=True,
    )

    sensor = models.CharField(
        _('Optical sensor'),
        max_length=255,
        null=True,
        blank=True
    )

    satellite = models.CharField(
        _('Satellite'),
        #!!! converter o nome do satellite para o identify
        max_length=255,
        null=True,
        blank=True
    )

    uf = models.CharField(
        _('State acronym'),
        max_length=255,
        blank=True
    )

    municipality = models.CharField(
        _('City name'),
        max_length=255,
        blank=True
    )

    geocod = models.CharField(
        _('Geo code'),
        max_length=255,
        blank=True
    )

    uc = models.CharField(
        _('Conserveation unit'),
        #???
        max_length=255,
        blank=True
    )

    publish_month= models.CharField(
        _('Publish month'),
        max_length=255,
        null=True,
        blank=True
    )

    no_ti = models.CharField(
        _('Indigenou Lands name'),
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

    geom = models.GeometryField(
        _('Geometry Field'),
        srid=4326,
        blank=True,
        null=True,
    )

    class Meta:
        """"Meta class for `deter_monitoring.DeterTI` model."""
        app_label = 'deter_monitoring'
        verbose_name = 'Deter Indigenous Lands'
        verbose_name_plural = 'Deter Indigenous Lands'
        # db_table = 'catalogo\".\"DeterTI'
        # managed = False
        ordering = ('-view_date', 'uf')

    def __str__(self) -> str:
        return str(self.view_date)

    def __str__(self) -> str:
        """Returns `deter_monitoring.DeterTI` string data.

        Returns:
            str: model data name.
        """
        return f'{self.path_row} - {self.view_date} - {self.classname}'