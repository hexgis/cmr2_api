from user import models as user_models
from layer.utils import validate_json_extension
from shapely.ops import unary_union
from urllib.parse import urljoin
from shapely.geometry import shape
from django.utils.translation import ugettext_lazy as _
from django.contrib.gis.geos import GEOSGeometry, WKBWriter, Polygon
from django.contrib.gis.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings
from urllib.request import urlopen
from colorfield.fields import ColorField
import xml.etree.ElementTree as ET
import requests
import json


class Geoserver(models.Model):
    """Model for Geoserver Data.

    * Association:
        * Inherits from :model:`models.Model`
        * Has many :model:`layer.Layer`
    """

    name = models.CharField(
        _('Name'),
        help_text=_('Geoserver Name'),
        max_length=255
    )

    wms_url = models.CharField(
        max_length=500,
        help_text=_('Default url to Web Map Service (WMS)')
    )

    preview_url = models.CharField(
        max_length=500,
        null=True,
        blank=True,
        help_text=_('Default url to request preview thumbnails')
    )

    thumbnail_url = models.URLField(
        _('Geoserver Thumbnail URL'),
        max_length=500,
        null=True,
        blank=True,
        help_text=_(
            'Default Geoserver URL in ' +
            'format https://**GEOSERVER**.com/geoserver/wms/reflect?'
        )
    )

    preview_url = models.URLField(
        _('Geoserver Preview URL'),
        max_length=500,
        null=True,
        blank=True,
        help_text=_(
            'Default Geoserver URL in ' +
            'format https://**GEOSERVER**.com/geoserver/' +
            'wms?REQUEST=GetLegendGraphic&VERSION=1.0.0&' +
            'FORMAT=image/png&WIDTH=40&HEIGHT=40'
        )
    )

    geoserver_url = models.URLField(
        _('Geoserver URL'),
        max_length=500,
        null=True,
        blank=True,
        help_text=_(
            'Default Geoserver URL in ' +
            'format https://**GEOSERVER**.com/geoserver/'
        )
    )

    def __str__(self):
        """Model class string.

        Returns:
            str: short description of Geoserver model.
        """

        return self.name

    class Meta:
        """Meta class for Geoserver model."""

        app_label = 'layer'
        verbose_name = 'Geoserver'
        verbose_name_plural = 'Geoservers'


class Basemap(models.Model):
    """Model for Basemap Data.

    * Association:
        * Inherits from :model:`models.Model`
    """

    url = models.CharField(
        _('Url'),
        help_text=_('ZXY url to map. Accepts //, http or https'),
        max_length=255,
        blank=True,
        null=True,
    )

    label = models.CharField(
        _('Label'),
        help_text=_('Label to show on app'),
        max_length=40,
        blank=True,
        null=True,
    )

    tag = models.CharField(
        _('Tag'),
        help_text=_('Tag to show on app'),
        max_length=40
    )

    attribution = models.CharField(
        _('Attribution'),
        help_text=_('Basemap attribution'),
        max_length=255,
        blank=True,
        null=True,
    )

    order = models.IntegerField(
        _('Order'),
        help_text=_('Basemap order on app'),
        default=1
    )

    def __str__(self):
        """Model class string.

        Returns:
            str: short description of Basemap model.
        """

        return f'{self.tag}: {self.label}'

    class Meta:
        """Meta class for Basemap model."""

        app_label = 'layer'
        ordering = ('order', 'id')


class Category(models.Model):
    """
    Model of Categories to group Layers Group
        * Association:
            * Inherits from :model:`models.Model`
            * Has many :model:`support.LayersGroup`
    """

    name = models.CharField(
        _('Name'),
        unique=True,
        max_length=25,
        null=True
    )

    icon = models.CharField(
        _('Icon'),
        max_length=255,
        default='layers',
        blank=True,
        null=True
    )

    description = models.CharField(
        _('Description'),
        max_length=1024,
        blank=True,
        null=True
    )

    class Meta:
        """Meta class for Layers Group model."""

        app_label = 'layer'
        ordering = ['name']

    def __str__(self):
        return self.name


class Group(models.Model):
    """Model for Layers group Data.

    * Association:
        * Inherits from :model:`models.Model`
        * Has many :model:`layer.Layer`
    """

    name = models.CharField(
        _('Name'),
        help_text=_('Group Layer name'),
        max_length=255,
        unique=True
    )

    category_groups = models.ForeignKey(
        Category,
        default=1,
        related_name='category',
        on_delete=models.DO_NOTHING
    )

    description = models.CharField(
        _('Description'),
        max_length=1024,
        blank=True,
        null=True
    )

    order = models.IntegerField(
        _('Order'),
        help_text=_('Order to show on app'),
        unique=False
    )

    def __str__(self) -> str:
        """Model class string.

        Returns:
            str: short description of Group model.
        """

        return self.name

    class Meta:
        """Meta class for Layers Group model."""

        app_label = 'layer'
        ordering = ['-order', '-id']


class Layer(models.Model):
    """Model for Layer Data.

    * Association:
        * Inherits from :model:`models.Model`
        * Has one :model:`layer.Geoserver`
        * Has one :model:`layer.Group`
    """

    name = models.CharField(
        _('Name'),
        max_length=255
    )

    order = models.IntegerField(
        _('Order'),
        blank=True,
        null=True
    )

    layer_type = models.CharField(
        _('Layer Type'),
        max_length=40
    )

    group = models.ForeignKey(
        'layer.Group',
        on_delete=models.DO_NOTHING,
        related_name='layers'
    )

    active_on_init = models.BooleanField(
        _('Active on Init'),
        help_text=_('Show layer as active when app starts'),
        default=False,
    )

    is_downloadable = models.BooleanField(
        _('Is Downloadable'),
        help_text=_('Enable layer download'),
        default=False
    )

    fonte = models.CharField(
        _('Fonte'),
        max_length=255,
        blank=True
    )

    is_public = models.BooleanField(
        _('Is Public'),
        default=False
    )

    dt_atualizacao = models.DateField(
        _('Atualização'),
        null=True,
        blank=True
    )

    database_layer_name = models.CharField(
        _('Database Layer Name'),
        max_length=255
    )

    bbox = models.GeometryField(
        srid=4326,
        blank=True,
        null=True
    )

    def __str__(self):
        """Model class string.

        Returns:
            str: short description of Layer model.
        """

        return f'{self.group.name} | {self.name}'

    class Meta:
        """Meta class for Layers model."""

        app_label = 'layer'
        ordering = ['-order']


class Tms(Layer):
    """Model for TMSLayer Data.

    * Association:
        * Inherits from :model:`models.Model`
        * Has one :model:`layer.Layer`
    """

    url = models.CharField(
        _('Tile Map Service Url'),
        max_length=500,
        blank=True,
        null=True
    )

    date = models.DateField(
        _('Date'),
        blank=True,
        null=True
    )

    max_native_zoom = models.IntegerField(
        _('Max Native Zoom'),
        blank=True,
        null=True
    )

    is_tms = models.BooleanField(
        _('Is a TMS Layer'),
        help_text=_('TMS layer = True. XYZ layer = False'),
        default=True
    )

    image_preview = models.FileField(
        _('Image preview'),
        blank=True,
        null=True,
    )

    thumbnail_blob = models.BinaryField(blank=True, null=True)

    legend = models.FileField(
        _('Legend'),
        blank=True,
        null=True,
    )

    legend_blob = models.BinaryField(blank=True, null=True)

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def save_image_preview(self):
        """Void method to update `Tms.legend_blob`."""

        try:
            if self.image_preview and self.image_preview.file:
                with self.image_preview.file as file:
                    content = file.read()
                self.thumbnail_blob = content
            else:
                print('File not found for preview save method.')
        except Exception as exc:
            print(f'[Error] Image preview error: {str(exc)}')

    def save_legend(self):
        """Void method to update `Tms.legend_blob`."""

        try:
            if self.legend and self.legend.file:
                with self.legend.file as file:
                    content = file.read()
                self.legend_blob = content
            else:
                print('File not found for preview save method.')
        except Exception as exc:
            print(f'[Error] Image preview error: {str(exc)}')

    def save(self, *args, **kwargs):
        """Validate and save the file."""

        self.full_clean()
        super(Tms, self).save(*args, **kwargs)

        self.save_image_preview()
        self.save_legend()

        super().save()

    def __str__(self):
        """Model class string.

        Returns:
            str: short description of Tms model.
        """

        return f'{self.url}'

    class Meta:
        """Meta class for Tms model."""

        app_label = 'layer'
        verbose_name = 'TMS'
        verbose_name_plural = 'TMS'


class Wms(Layer):
    """Model for WMSLayer Data.

    * Association:
        * Inherits from :model:`models.Model`
        * Has one :model:`layer.Geoserver`
        * Has one :model:`layer.Layer`
    """

    PREVIEW_TYPE_OPTIONS = [
        ('thumbnail', 'Thumbnail'),
        ('preview', 'Preview'),
    ]

    TYPE_OPTIONS = [
        ('Raster', 'Raster'),
        ('Point', 'Point'),
        ('Point-Icon', 'Point-Icon'),
        ('Line', 'Line'),
        ('Polygon', 'Polygon'),
        ('Video', 'Video'),
    ]

    has_preview = models.BooleanField(
        _('Has Preview'),
        help_text=_('Show layer thumbnails on app'),
        default=True
    )

    has_detail = models.BooleanField(
        _('Has Detail'),
        help_text=_('Show layer legend on app'),
        default=False
    )

    detail_width = models.IntegerField(
        _('Detail width'),
        help_text=_('Max width for legend on app'),
        blank=True,
        null=True
    )

    geoserver = models.ForeignKey(
        'layer.Geoserver',
        on_delete=models.DO_NOTHING,
        related_name='layers',
        blank=False,
        null=True
    )

    geoserver_layer_name = models.CharField(
        _('Geoserver Layer Name'),
        help_text=_('Geoserver layer name'),
        max_length=255,
        blank=True,
        null=True
    )

    geoserver_layer_namespace = models.CharField(
        _('Geoserver Layer Namespace'),
        help_text=_('Geoserver layer namespace'),
        max_length=40,
        blank=True,
        null=True)

    geoserver_layer_options = models.JSONField(
        ('Geoserver Layer Options'),
        help_text=_('Geoserver layer extra options'),
        blank=True,
        null=True
    )

    queryable = models.BooleanField(
        _('Is queryable'),
        help_text=_('Shows popup attribution on app'),
        default=True
    )

    has_opacity = models.BooleanField(
        _('Has opacity'),
        help_text=_('Shows opacity label on app'),
        default=True
    )

    default_opacity = models.PositiveIntegerField(
        _('Default opacity'),
        help_text=_('Default value opacity between 0 and 100'),
        blank=True,
        null=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )

    has_sublayers = models.BooleanField(
        _('Has Sublayers'),
        help_text=_('Shows sublayers on app'),
        default=False
    )

    wms_layer_type = models.CharField(
        _('WMS Layer Type'),
        max_length=40,
        choices=TYPE_OPTIONS,
        default='Polygon',
    )

    preview_type = models.CharField(
        _('Preview type'),
        choices=PREVIEW_TYPE_OPTIONS,
        default='thumbnail',
        help_text=_('Layer preview/thumbnail type'),
        max_length=40,
        blank=True,
        null=True
    )

    thumbnail_blob = models.BinaryField(blank=True, null=True)

    has_metadata = models.BooleanField(
        _('Has Metadata'),
        help_text=_('Has metadata attributes on Geoserver'),
        default=False
    )

    def get_thumbnail_blob(self):
        """ et `WMSLayer.thumbnail_blob` from geoserver."""

        try:
            if self.preview_type == 'thumbnail' \
               and self.geoserver.thumbnail_url:
                url = (
                    f'layers='
                    f'{self.geoserver_layer_namespace}:'
                    f'{self.geoserver_layer_name}'
                    f'&width=60'
                )

                if 'authkey=' in self.geoserver.thumbnail_url:
                    url = \
                        f'{self.geoserver.thumbnail_url}&{url}'
                else:
                    url = \
                        f'{self.geoserver.thumbnail_url}?{url}'

            if self.preview_type == 'preview' and self.geoserver.preview_url:
                url = (
                    f'{self.geoserver.preview_url}'
                    f'{self.geoserver_layer_namespace}'
                    f':{self.geoserver_layer_name}'
                )

            response = urlopen(url)
            self.thumbnail_blob = response.read()
        except Exception as exc:
            print(exc)

    def get_bbox(self):
        """Get `WMSLayer.bbox` from geoserver."""

        try:
            url = urljoin(
                self.geoserver.geoserver_url,
                (
                    f'{self.geoserver_layer_namespace}' + '/' +
                    f'{self.geoserver_layer_name}' +
                    '/wms?service=WMS&version=1.1.0&request=GetCapabilities'
                )
            )

            response = requests.get(url, timeout=settings.TIMEOUT)
            print(response.url)

            if response.ok:
                bbox = ET.fromstring(
                    response.content
                ).find('.//LatLonBoundingBox')

                if bbox is not None:
                    self.bbox = Polygon.from_bbox((
                        float(bbox.attrib.get('minx')),
                        float(bbox.attrib.get('miny')),
                        float(bbox.attrib.get('maxx')),
                        float(bbox.attrib.get('maxy'))
                    ))
            else:
                print(f'[Error] Getting data from url: {response.url}')

        except Exception as exc:
            print(f'[Error] Fetching {self} bbox: {exc}.')

    def save(self, *args, **kwargs):
        """Override method of saving data in `models.Layer`"""

        if not self.bbox:
            self.get_bbox()

        if (self.has_preview or self.has_detail) and not self.thumbnail_blob:
            self.get_thumbnail_blob()

        super().save(*args, **kwargs)

    def __str__(self):
        """Model class string.

        Returns:
            str: short description of Wms model.
        """

        return f'{self.geoserver_layer_namespace}:{self.geoserver_layer_name}'

    class Meta:
        """Meta class for Tms model."""

        app_label = 'layer'
        verbose_name = 'WMS'
        verbose_name_plural = 'WMS'


class Vector(Layer):
    """Model for Vector Data.

    * Association:
        * Inherits from :model:`Layer`
    """

    TYPE_OPTIONS = [
        ('Raster', 'Raster'),
        ('Point', 'Point'),
        ('Point-Icon', 'Point-Icon'),
        ('Line', 'Line'),
        ('Polygon', 'Polygon'),
        ('Video', 'Video'),
        ('streaming', 'Streaming'),
    ]

    file = models.FileField(
        _('File Path'),
        blank=True,
        null=True,
        validators=[validate_json_extension]
    )

    description = models.TextField(
        _('Description'),
        blank=True,
        null=True
    )

    type = models.CharField(
        _('Vector Layer Type'),
        max_length=40,
        choices=TYPE_OPTIONS,
        default='Polygon',
    )

    color = ColorField(
        _('Color'),
        default='#3388FF',
    )

    color_fill = ColorField(
        _('Color Fill'),
        default='#3388FF',
    )

    has_opacity = models.BooleanField(
        _('Has opacity'),
        help_text=_('Shows opacity label on app'),
        default=True
    )

    default_opacity = models.PositiveIntegerField(
        _('Default opacity'),
        help_text=_('Default value opacity between 0 and 100'),
        blank=True,
        null=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )

    image_preview = models.FileField(
        _('Image preview'),
        blank=True,
        null=True,
    )

    thumbnail_blob = models.BinaryField(blank=True, null=True)

    def _handle_geojson_geometry(
        self,
        geometry: dict,
        properties: dict
    ) -> 'VectorGeometry':
        """Creates a `VectorGeometry` from geojson geometry.

        Args:
            geometry (dict): GeoJSON geometry data.
            properties (dict): Geometry properties.

        Returns:
            VectorGeometry: VectorGeometry model data.
        """

        if geometry:
            geom = GEOSGeometry(json.dumps(geometry))
            wkb_w = WKBWriter()
            wkb_w.outdim = 2
            geom = GEOSGeometry(wkb_w.write(geom), srid=geom.srid)

            vector, _ = VectorGeometry.objects.get_or_create(
                vector_uploaded=self,
                geom=geom,
                properties=properties
            )

        return vector

    def _check_filepath_exists(self) -> bool:
        """Check if file path exists on os.

        Returns:
            bool: file path exists.
        """

        return bool(self.file.name) and \
            self.file.storage.exists(self.file.name)

    def save_geojson_to_geometry(self):
        """Convert JSON file to list of `models.Vector`."""

        if not self._check_filepath_exists():
            if self.vector_geometry.count():
                return True
        else:
            with open(self.file.path, 'r', encoding='utf-8') as geojson_file:
                geojson_data = geojson_file.read()
                geometries = []
                try:
                    geojson_data = json.loads(geojson_data)
                    geometries = []
                    for feature in geojson_data.get('features', []):
                        self._handle_geojson_geometry(
                            geometry=feature.get('geometry', None),
                            properties=feature.get('properties', {})
                        )
                        geometries.append(shape(feature.get('geometry', None)))

                    self.bbox = Polygon.from_bbox(
                        unary_union(geometries).bounds
                    )

                except json.JSONDecodeError as decode_error:
                    print(
                        f'[Error] GeoJSON decode error: {str(decode_error)}')

    def save_image_preview(self):
        """Void method to update `Vector.thumbnail_blob`."""

        try:
            if self.image_preview and self.image_preview.file:
                with self.image_preview.file as file:
                    content = file.read()
                self.thumbnail_blob = content
            else:
                print('File not found for preview save method.')
        except Exception as exc:
            print(f'[Error] Image preview error: {str(exc)}')

    def save(self, *args, **kwargs):
        """Validate and save the file."""

        self.full_clean()
        super(Vector, self).save(*args, **kwargs)

        self.save_geojson_to_geometry()
        self.save_image_preview()

        super().save()

    class Meta:
        """Meta class for Vector model."""

        app_label = 'layer'
        verbose_name = 'Vector'
        verbose_name_plural = 'Vectors'


class VectorGeometry(models.Model):
    """Model to store user uploaded file geometries."""

    vector_uploaded = models.ForeignKey(
        Vector,
        on_delete=models.CASCADE,
        related_name='vector_geometry',
    )

    geom = models.GeometryField(srid=4326)

    properties = models.JSONField(
        _('Properties'),
        help_text=_('Uploaded file properties.'),
        blank=True,
        null=True
    )

    def __str__(self):
        """Model class string.

        Returns:
            str: short description of VectorGeometry model.
        """

        return f'{self.vector_uploaded}'

    class Meta:
        """Meta class for VectorGeometry model."""

        app_label = 'layer'
        verbose_name_plural = 'Vector Geometries'


class Filter(models.Model):
    """Model for Filter Data.

    * Association:
        * Inherits from :model:`models.Model`
        * Has many :model:`layer.Layer`
    """

    default = models.CharField(
        _('Default value for filters'),
        help_text=_('Shows default value for filter on app'),
        max_length=40,
        blank=True,
        null=True,
    )

    alias = models.CharField(
        _('Filter alias'),
        help_text=_('Indicates which field will be filtered on app'),
        max_length=255,
        blank=True,
        null=True,
    )

    type = models.CharField(
        _('Filter Type'),
        help_text=_('Type of filter on app'),
        max_length=40
    )

    label = models.CharField(
        _('Filter Label'),
        help_text=_('A default label for filter'),
        max_length=40
    )

    layers = models.ManyToManyField(
        Layer,
        related_name='filters',
        blank=True
    )

    def __str__(self):
        """Model class string.

        Returns:
            str: short description of Filter model.
        """

        return f'{self.label}:{self.type}'

    class Meta:
        """Meta class for Filter model."""

        app_label = 'layer'


class ManagementInstrument(models.Model):
    """Instrumental Indigenous Lands model data.

    * Association:
        * Has one: `funai.LimiteTerraIndigena`
    """

    co_funai = models.IntegerField(
        _('Cod Funai'),
        blank=False,
        null=False
    )
    no_ti = models.CharField(
        _('Terras Indígena'),
        max_length=255,
        blank=True,
        null=True
    )
    no_regiao = models.CharField(
        _('Região'),
        max_length=255,
        blank=True,
        null=True
    )
    sg_uf = models.CharField(
        _('UF'),
        max_length=255,
        blank=True,
        null=True
    )
    no_povo = models.CharField(
        _('Povos'),
        max_length=255,
        blank=True,
        null=True
    )
    no_bioma = models.CharField(
        _('Bioma'),
        max_length=255,
        blank=True,
        null=True
    )
    ds_parceiros = models.CharField(
        _('Parceiros'),
        max_length=255,
        blank=True,
        null=True
    )
    cr_funai = models.CharField(
        _('Nome Funai'),
        max_length=255,
        blank=True,
        null=True
    )
    no_ig = models.CharField(
        _('Instrumento'),
        max_length=255,
        blank=True,
        null=True
    )
    ds_status = models.CharField(
        _('Status'),
        max_length=255,
        blank=True,
        null=True
    )
    nu_ano_elaboracao = models.IntegerField(
        _('Elaborado em'),
        blank=True,
        null=True
    )
    ds_disp_meio_local = models.CharField(
        _('Disponível em'),
        max_length=255,
        blank=True,
        null=True
    )
    ds_tll_publi = models.CharField(
        _(''),
        max_length=255,
        blank=True,
        null=True
    )
    ds_obs = models.CharField(
        _('Observação'),
        max_length=255,
        blank=True,
        null=True
    )
    dt_cadastro = models.DateField(
        _('Data Registro'),
        blank=True,
        null=True
    )

    class Meta:
        app_label = 'layer'
        verbose_name = _('Management Instrument')
        verbose_name_plural = _('Management Instruments')
