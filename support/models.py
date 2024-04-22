from django.contrib.gis.db import models
from django.utils.translation import ugettext_lazy as _
from datetime import datetime


class Geoserver(models.Model):
    """
    Model for Geoserver Data
        * Association:
            * Inherits from :model:`models.Model`
            * Has many :model:`support.Layer`
    """

    name = models.CharField(
        _('Name'),
        max_length=255
    )

    wms_url = models.CharField(
        _('Wms URL'),
        max_length=500
    )

    preview_url = models.CharField(
        _('Preview URL'),
        max_length=500,
        null=True,
        blank=True
    )

    class Meta:
        app_label = 'support'
        verbose_name = 'Geoserver'
        verbose_name_plural = 'Geoservers'

    def __str__(self):
        return self.name


class CategoryLayersGroup(models.Model):
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
        app_label = 'support'
        verbose_name = 'Category Groups Layers'
        verbose_name_plural = 'Categories Groups Layers'
        ordering = ['name']

    def __str__(self):
        return self.name


class LayersGroup(models.Model):
    """
    Model for categorization of Layers Data
        * Association:
            * Inherits from :model:`models.Model`
            * Has many :model:`support.Layer`
    """

    name = models.CharField(
        _('Name'),
        max_length=255,
        unique=True
    )

    order = models.IntegerField(
        _('Order'),
        unique=True
    )

    category_groups = models.ForeignKey(
        CategoryLayersGroup,
        default=1,
        related_name='category',
        on_delete=models.DO_NOTHING
    )

    class Meta:
        app_label = 'support'
        verbose_name = 'Layers Group'
        verbose_name_plural = 'Layers Groups'
        ordering = ['-order']

    def __str__(self):
        return self.name


class Layer(models.Model):
    """
    Model for Layer Data
        * Association:
            * Inherits from :model:`models.Model`
            * Has one :model:`support.Geoserver`
            * Has one :model:`support.LayersGroup`
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

    layers_group = models.ForeignKey(
        LayersGroup,
        on_delete=models.DO_NOTHING,
        related_name='layers',
        null=True,
        blank=True
    )

    active_on_init = models.BooleanField(
        _('Active on Init'),
        default=False,
    )

    is_public = models.BooleanField(
        _('Geoservice is Public'),
        default=False
    )

    class Meta:
        app_label = 'support'
        verbose_name = 'Layer'
        verbose_name_plural = 'Layers'
        ordering = ['-order']

    def __str__(self):
        return self.name


class LayersInfo(models.Model):
    """
    Model for Layers Info Data
        * Association:
            * Inherits from :model:`models.Model`
    """
    fonte = models.CharField(
        _('Fonte'),
        max_length=255,
        blank=True
    )

    layer_id = models.OneToOneField(
        Layer,
        on_delete=models.DO_NOTHING,
        related_name='layer_info'
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

    class Meta:
        app_label = 'support'
        verbose_name = 'Layer Info'
        verbose_name_plural = 'Layers Info'

    def __str__(self):
        return self.name


class WmsLayer(models.Model):
    """
    Model for WMSLayer Data
        * Association:
            * Inherits from :model:`models.Model`
            * Has one :model:`support.Geoserver`
            * Has one :model:`support.Layer`
    """

    has_preview = models.BooleanField(
        _('Has preview'),
        default=True
    )

    has_detail = models.BooleanField(
        _('Has detail'),
        default=False
    )

    detail_width = models.IntegerField(
        _('Detail width'),
        blank=True,
        null=True
    )

    geoserver = models.ForeignKey(
        'support.Geoserver',
        on_delete=models.DO_NOTHING,
        related_name='layers',
        blank=True,
        null=True
    )

    geoserver_layer_name = models.CharField(
        _('Geoserver Layer Name'),
        max_length=255,
        blank=True,
        null=True
    )

    geoserver_layer_namespace = models.CharField(
        _('Geoserver Layer Namespace'),
        max_length=40,
        blank=True,
        null=True)

    layer = models.OneToOneField(
        Layer,
        on_delete=models.DO_NOTHING,
        primary_key=True,
        related_name='wms'
    )

    geoserver_layer_options = models.JSONField(
        _('Geoserver Layer Options'),
        blank=True,
        null=True
    )

    queryable = models.BooleanField(
        _('WmsLayer is queryable'),
        default=True
    )

    has_opacity = models.BooleanField(
        _('Has opacity'),
        default=True
    )

    default_opacity = models.IntegerField(
        _('Default opacity'),
        blank=True,
        null=True
    )

    class Meta:
        app_label = 'support'
        verbose_name = 'WMS Layer'
        verbose_name_plural = 'WMS Layers'

    def __str__(self):
        return "{}:{}".format(
            self.geoserver_layer_namespace,
            self.geoserver_layer_name
        )


class TmsLayer(models.Model):
    """
    Model for TMSLayer Data
        * Association:
            * Inherits from :model:`models.Model`
            * Has one :model:`support.Layer`
    """

    url_tms = models.CharField(
        _('URL TMS'),
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

    layer = models.OneToOneField(
        Layer,
        on_delete=models.DO_NOTHING,
        primary_key=True,
        related_name='tms'
    )

    class Meta:
        app_label = 'support'
        verbose_name = 'TMS Layer'
        verbose_name_plural = 'TMS Layers'

    def __str__(self):
        return self.url_tms


class LayerFilter(models.Model):
    """
    Model for LayerFilter Data
        * Association:
            * Inherits from :model:`models.Model`
            * Has many :model:`support.Layer`
    """

    default = models.CharField(
        _('Default value for filters'),
        max_length=40,
        blank=True,
        null=True,
    )

    filter_type = models.CharField(
        _('Filter Type'),
        max_length=40
    )

    label = models.CharField(
        _('Filter Label'),
        max_length=40
    )

    filter_alias = models.CharField(
        _('Filter WMS services'),
        max_length=40
    )

    layers = models.ManyToManyField(
        Layer,
        related_name='layer_filters'
    )

    class Meta:
        app_label = 'support'
        verbose_name = 'Layer Filter'
        verbose_name_plural = 'Layer Filters'

    def __str__(self):
        return "{}: {}".format(self.label, self.filter_alias)


class CoordenacaoRegional(models.Model):

    co_cr = models.BigIntegerField(
        _('Regional Coordenation code'),
        unique=True,
        default=1
    )

    ds_email = models.CharField(
        _('Email'),
        max_length=150,
        blank=True,
        null=True
    )

    ds_telefone = models.TextField(
        _('Contact number'),
        blank=True,
        null=True
    )

    dt_cadastro = models.DateTimeField(
        _('Register date'),
        default=datetime.now,
        blank=True,
        null=True
    )

    geom = models.PointField(srid=4674)

    no_abreviado = models.CharField(
        _('Regional Coordenation acronym'),
        max_length=50,
        blank=True,
        null=True
    )

    no_cr = models.CharField(
        max_length=100
    )

    no_municipio = models.CharField(
        _('City name'),
        max_length=100,
        blank=True,
        null=True
    )

    no_regiao = models.CharField(
        _('Region name'),
        max_length=12,
        blank=True,
        null=True
    )

    no_uf = models.CharField(
        _('State'),
        max_length=50,
        blank=True,
        null=True
    )

    sg_cr = models.CharField(
        _('Regional Coordenation flag'),
        max_length=20,
        blank=True,
        null=True
    )

    sg_uf = models.CharField(
        _('State acronym'),
        max_length=2,
        blank=True,
        null=True
    )

    st_situacao = models.CharField(
        _('Situation'),
        max_length=10,
        blank=True,
        null=True
    )

    def __str__(self):
        return str(self.no_cr)

    class Meta:
        """Metaclass to `funai.CoordenacaoRegional`."""
        app_label = 'support'
        verbose_name = 'Regional Coordinations'
        verbose_name_plural = 'Regional Coordinations'
        ordering = ['no_cr']


class TerraIndigena(models.Model):
    geom = models.MultiPolygonField(srid=4674)
    no_ti = models.CharField(
        _('Name of Indigenous Lands'),
        max_length=255,
    )
    co_funai = models.IntegerField(
        _('Funai code'),
        unique=True,
    )
    no_grupo_etnico = models.CharField(_("Grupo Étnico"), max_length=255)
    ds_fase_ti = models.CharField(_("Fase TI"), max_length=100)
    ds_modalidade = models.CharField(_("Modalidade TI"), max_length=100)
    ds_reestudo_ti = models.CharField(_("Reestudo TI"), max_length=80)
    ds_cr = models.CharField(max_length=100)
    co_cr = models.ForeignKey(
        CoordenacaoRegional,
        to_field='co_cr',
        related_name='terras_indigenas',
        on_delete=models.DO_NOTHING,
        db_column='co_cr',
        db_constraint=False
    )
    no_municipio = models.TextField()
    sg_uf = models.CharField(max_length=20)
    st_faixa_fronteira = models.CharField(max_length=3)
    dt_em_estudo = models.DateField()
    ds_portaria_em_estudo = models.TextField()
    dt_delimitada = models.DateField()
    ds_despacho_delimitada = models.TextField()
    dt_declarada = models.DateField()
    ds_portaria_declarada = models.TextField()
    dt_homologada = models.DateField()
    ds_decreto_homologada = models.TextField()
    dt_regularizada = models.DateField()
    ds_matricula_regularizada = models.TextField()
    ds_doc_resumo_em_estudo = models.TextField()
    ds_doc_resumo_delimitada = models.TextField()
    ds_doc_resumo_declarada = models.TextField()
    ds_doc_resumo_homologada = models.TextField()
    ds_doc_resumo_regularizada = models.TextField()
    st_amazonia_legal = models.BooleanField()
    nu_area_ha = models.DecimalField(max_digits=100, decimal_places=2)
    dt_cadastro = models.DateTimeField()

    def __str__(self):
        return str(self.no_ti)

    class Meta:
        """Metaclass to `funai.LimiteTerraIndigena`."""
        app_label = 'support'
        verbose_name = _('Indigenous Lands')
        verbose_name_plural = _('Indigenous Lands')
        ordering = ['no_ti']
