from django.contrib.gis.db import models

from django.utils.translation import ugettext_lazy as _


class Satellite(models.Model):
    """Model to store satellite information."""

    identifier = models.CharField(
        _('Identifier'),
        max_length=255,
        unique=True
    )

    name = models.CharField(
        _('Satellite name'),
        max_length=255,
        blank=True,
        null=True
    )

    description = models.TextField(
        _('Description'),
        max_length=511,
        blank=True,
        null=True
    )

    class Meta:
        """"Meta class for `catalog.Satellite` model."""
        app_label = 'catalog'
        verbose_name = 'Satellite'
        verbose_name_plural = 'Satellites'
        ordering = ('name',)

    def __str__(self) -> str:
        """Returns `catalog.Satellite` string data.

        Returns:
            str: model data identifier.
        """
        return str(self.name) or str(self.identifier)


class Catalogs(models.Model):
    """Model for db view aggregating all satellite scene catalog."""

    objectid = models.AutoField(
        _('Object id'),
        primary_key=True
    )

    image = models.CharField(
        _('Product scene'),
        max_length=255,
        unique=True
    )

    type = models.CharField(
        _('Type'),
        max_length=255,
        null=True,
        blank=True
    )

    image_path = models.CharField(
        _('Image repository'),
        max_length=511
    )

    url_tms = models.CharField(
        _('Tile file link'),
        max_length=511
    )

    date = models.DateField(
        _('Scene Date')
    )

    pr_date = models.DateField(
        _('Process Date'),
    )

    cloud_cover = models.FloatField(
        _('Percentage of cloud cover'),
        null=True,
        default=0
    )

    locator = models.CharField(
        _('Satellite scene parameters'),
        max_length=255,
        null=True
    )

    max_native_zoom = models.IntegerField(
        _('Maximum zoom scale'),
        default=15,
    )

    sat_identifier = models.CharField(
        _('Satellite identifier'),
        max_length=255,
        null=True,
        blank=True
    )

    sat_name = models.CharField(
        _('Satellite name'),
        max_length=255,
        null=True,
        blank=True
    )

    preview = models.TextField(
        _('Image preveiw link'),
        max_length=511,
        null=True,
        blank=True
    )

    geom = models.PolygonField(
        _('Geometry Field'),
        srid=4674,
        null=True,
        blank=True
    )

    class Meta:
        """"Meta class for `catalog.Catalogs` abstract model."""
        app_label = 'catalog'
        verbose_name = 'Catalog Scene'
        verbose_name_plural = 'Catalogs Scenes'
        db_table = 'catalogo\".\"vw_img_catalogo_a'
        managed = False
        ordering = ('-date', )

    def __str__(self) -> str:
        return str(self.image)
