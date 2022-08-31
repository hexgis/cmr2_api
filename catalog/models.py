# from django.db import models
from django.contrib.gis.db import models

from django.utils.translation import ugettext_lazy as _


class Satellite (models.Model):
    '''Model to store satellite information.'''

    identifier = models.CharField(
        _('Identifier'),
        max_length=40,
        unique=True,
    )

    name = models.CharField(
        _('Name Satellite'),
        max_length=255,
        blank=True,  # blank=False,
        null=True,  # null=False,
    )

    description = models.TextField(
        _('Description'),
        max_length=511,
        blank=True,
        null=True,
    )

    def __str__(self) -> str:
        return self.name or self.identifier


class Catalogs (models.Model):
    # objectid = models.AutoField(
    #     _(''),
    #     primary_key=True
    # )

    image = models.CharField(
        _('Color composition name'),
        max_length=255,
        unique=True
    )

    product = models.CharField(
        _('Product scene'),
        max_length=255,
        null=True,
        blank=True
    )

    satellite = models.ForeignKey(
        'catalog.Satellite',
        null=True,
        blank=True,
        # on_delete=models.CASCADE,
        on_delete=models.DO_NOTHING,
        # related_name='catalog_satellite'
        # related_name="%(app_label)s_%(class)s_status",
        # related_query_name="%(app_label)s_%(class)ss"
    )

    type = models.CharField(
        _('Composition type'),
        max_length=30,
        null=True,
        blank=True
    )

    date = models.DateField(
        _('Scene Date')
    )

    cloud_cover = models.FloatField(
        _('Percentage of cloud cover'),
        null=True,
    )

    url_tms = models.CharField(
        _('Tile path'),
        max_length=511
    )

    path = models.CharField(
        _('Image repository'),
        max_length=511,
    )

    download_link = models.CharField(
        _('Image repository'),
        max_length=511,
    )

    download_available = models.BooleanField(
        _("Download allowed"),
        default=False,

    )

    max_native_zoom = models.IntegerField(
        _('Maximum zoom scale'),
        default=15,

    )

    # geom = models.PolygonField(
    geom = models.GeometryField(
        _('Geometry Field'),
        srid=4674,
        null=True,
        blank=True,
    )

    class Meta:
        abstract = True
        ordering = ['-data']

    def __str__(self):
        return str(self.image)


class Landsat8Catalog (Catalogs):
    """Model for Landsat scenes catalog."""

    orbita = models.CharField(
        _('Satellite Path'),
        max_length=3,
        null=True,
        blank=True,
    )

    ponto = models.CharField(
        _('Satellite Row'),
        max_length=3,
        null=True,
        blank=True,
    )

    class Meta:
        """"Meta class for `catalog.Landsat8Catalog` model."""
        app_label = 'catalog'
        verbose_name = 'Landsat8 Catalog'
        verbose_name_plural = 'Landsat8 Catalogs'


class Sentinel2Catalog (Catalogs):
    """Model for Sentinel 2 scenes catalog."""

    utm_zone = models.IntegerField(
        _('UTM Zone'),
        null=True,
        blank=True,
    )

    latitude_band = models.CharField(
        _('Latitude Band'),
        max_length=255,
        null=True,
        blank=True,
    )

    grid_square = models.CharField(
        _('Grid Square'),
        max_length=255,
        null=True,
        blank=True,
    )

    class Meta:
        """"Meta class for `catalog.Sentinel2Catalog` model."""
        app_label = 'catalog'
        verbose_name = 'Sentinel2 Catalog'
        verbose_name_plural = 'Sentinel2 Catalogs'
