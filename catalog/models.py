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


class Catalog(models.Model):
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
        _('Tile file'),
        max_length=511
    )

    date = models.DateTimeField(
        _('Scene Date')
    )

    pr_date = models.DateField(
        _('Process Date'),
        auto_now_add=True
    )

    cloud_cover = models.FloatField(
        _('Percentage of cloud cover'),
        null=True,
        default=0
    )

    locator = models.CharField(
        _(''),
        max_length=255,
        null=True
    )

    max_native_zoom = models.IntegerField(
        _('Maximum zoom scale'),
        default=15
    )

    sat = models.ForeignKey(
        Satellite,
        on_delete=models.DO_NOTHING,
        related_name='+'
    )

    preview = models.TextField(
        _(''),
        max_length=511,
        null=True,
        blank=True
    )

    # geom = models.GeometryField(
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
        # abstract = True
        # db_table = 'catalogo\".\"vw_img_catalogo_a'
        # managed = False
        ordering = ('-date', )

    def __str__(self) -> str:
        return str(self.image)


# class Catalogs(models.Model):
#     """Abstract model for Catalogs"""

#     image = models.CharField(
#         _('Color composition name'),
#         max_length=255,
#         unique=True
#     )

#     product = models.CharField(
#         _('Product scene'),
#         max_length=255,
#         null=True,
#         blank=True
#     )

#     satellite = models.ForeignKey(
#         'catalog.Satellite',
#         null=True,
#         blank=True,
#         on_delete=models.DO_NOTHING,
#     )

#     type = models.CharField(
#         _('Composition type'),
#         max_length=30,
#         null=True,
#         blank=True
#     )

#     date = models.DateField(
#         _('Scene Date')
#     )

#     cloud_cover = models.FloatField(
#         _('Percentage of cloud cover'),
#         null=True,
#     )

#     url_tms = models.CharField(
#         _('Tile path'),
#         max_length=511
#     )

#     path = models.CharField(
#         _('Image repository'),
#         max_length=511,
#     )

#     download_link = models.CharField(
#         _('Image repository'),
#         max_length=511,
#     )

#     download_available = models.BooleanField(
#         _("Download allowed"),
#         default=False,
#     )

#     max_native_zoom = models.IntegerField(
#         _('Maximum zoom scale'),
#         default=15,
#     )

#     co_cr = models.BigIntegerField(
#         _('Regional Coordenation code'),
#     )

#     ds_cr = models.CharField(
#         _('Regional Coordenation name'),
#         max_length=255,
#     )

#     co_funai = models.IntegerField(
#         _('Funai code'),
#     )

#     no_ti = models.CharField(
#         _('Name of Indigenous Lands'),
#         max_length=255,
#     )

#     municipio = models.CharField(
#         _('County'),
#         max_length=255,
#         blank=True,
#         null=True
#     )

#     sg_uf = models.CharField(
#         _('State aconymn'),
#         max_length=255,
#         blank=True,
#         null=True
#     )

#     resolution = models.IntegerField(
#         _('Spatial resolution'),
#         null=True,
#         blank=True,
#     )

#     nu_latitude = models.CharField(
#         _('Numero latitude'),
#         max_length=255,
#         blank=True,
#         null=True
#     )

#     nu_longitude = models.CharField(
#         _('Numero longitude'),
#         max_length=255,
#         blank=True,
#         null=True
#     )

#     # geom = models.PolygonField(
#     geom = models.GeometryField(
#         _('Geometry Field'),
#         srid=4674,
#         null=True,
#         blank=True,
#     )

#     class Meta:
#         """"Meta class for `catalog.Catalogs` abstract model."""
#         app_label = 'catalog'
#         verbose_name = 'Abastract Catalog'
#         verbose_name_plural = 'Abastract Catalogs'
#         abstract = True
#         ordering = ['-data']

#     def __str__(self) -> str:
#         """Returns `catalog.Catalogs` string data.

#         Returns:
#             str: model data image.
#         """
#         return str(self.image)


# class Landsat8Catalog(Catalogs):
#     """Model for Landsat scenes catalog."""

#     orbita = models.CharField(
#         _('Satellite Path'),
#         max_length=3,
#         null=True,
#         blank=True,
#     )

#     ponto = models.CharField(
#         _('Satellite Row'),
#         max_length=3,
#         null=True,
#         blank=True,
#     )

#     class Meta:
#         """"Meta class for `catalog.Landsat8Catalog` model."""
#         app_label = 'catalog'
#         verbose_name = 'Landsat8 Catalog'
#         verbose_name_plural = 'Landsat8 Catalogs'


# class Sentinel2Catalog(Catalogs):
#     """Model for Sentinel-2 scenes catalog."""

#     utm_zone = models.IntegerField(
#         _('UTM Zone'),
#         null=True,
#         blank=True,
#     )

#     latitude_band = models.CharField(
#         _('Latitude Band'),
#         max_length=255,
#         null=True,
#         blank=True,
#     )

#     grid_square = models.CharField(
#         _('Grid Square'),
#         max_length=255,
#         null=True,
#         blank=True,
#     )

#     class Meta:
#         """"Meta class for `catalog.Sentinel2Catalog` model."""
#         app_label = 'catalog'
#         verbose_name = 'Sentinel2 Catalog'
#         verbose_name_plural = 'Sentinel2 Catalogs'
