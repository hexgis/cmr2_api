from django.contrib.gis.db import models
from django.utils.translation import ugettext_lazy as _


class Geoserver(models.Model):
    """
    Model for Geoserver Data
        * Association:
            * Inherits from :model:`models.Model`
            * Has many :model:`support.Layer`
    """

    name = models.CharField(
        _("Name"),
        max_length=255
    )

    wms_url = models.CharField(
        max_length=500
    )

    preview_url = models.CharField(
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


class LayersGroup(models.Model):
    """
    Model for Layers group Data
        * Association:
            * Inherits from :model:`models.Model`
            * Has many :model:`support.Layer`
    """

    name = models.CharField(
        _("Name"),
        max_length=255,
        unique=True
    )

    order = models.IntegerField(
        _("Order"),
        unique=True
    )

    icon = models.CharField(
        _("Icon"),
        max_length=255,
        default="layers",
        blank=True,
        null=True
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
        _("Name"),
        max_length=255
    )

    order = models.IntegerField(
        _("Order"),
        blank=True,
        null=True
    )

    layer_type = models.CharField(
        _("Layer Type"),
        max_length=40
    )

    layers_group = models.ForeignKey(
        'support.LayersGroup',
        on_delete=models.DO_NOTHING,
        related_name='layers',
        null=True,
        blank=True
    )

    active_on_init = models.BooleanField(
        _("Active on Init"),
        default=False,
    )

    class Meta:
        app_label = 'support'
        verbose_name = 'Layer'
        verbose_name_plural = 'Layers'
        ordering = ['-order']

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
        default=True
    )

    has_detail = models.BooleanField(
        default=False
    )

    detail_width = models.IntegerField(
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
        _("Geoserver Layer Name"),
        max_length=255,
        blank=True,
        null=True
    )

    geoserver_layer_namespace = models.CharField(
        _("Geoserver Layer Namespace"),
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
        ("Geoserver Layer Options"),
        blank=True,
        null=True
    )

    queryable = models.BooleanField(
        default=True
    )

    has_opacity = models.BooleanField(
        default=True
    )

    default_opacity = models.IntegerField(
        blank=True,
        null=True
    )

    class Meta:
        app_label = 'support'
        verbose_name = 'WmsLayer'
        verbose_name_plural = 'WmsLayers'

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
        max_length=500,
        blank=True,
        null=True
    )

    date = models.DateField(
        _("Date"),
        blank=True,
        null=True
    )

    max_native_zoom = models.IntegerField(
        _("Max Native Zoom"),
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
        verbose_name = 'TmsLayer'
        verbose_name_plural = 'TmsLayers'

    def __str__(self):
        return self.url_tms


class HeatmapLayer(models.Model):
    """
    Model for HeatmapLayer Data
        * Association:
            * Inherits from :model:`models.Model`
            * Has one :model:`support.Layer`
    """

    # heatmap_type = models.IntegerField(
    #     on_delete=models.CASCADE,
    #     null=True,
    #     blank=True
    # )

    layer = models.OneToOneField(
        Layer,
        on_delete=models.DO_NOTHING,
        primary_key=True,
        related_name='heatmap'
    )

    class Meta:
        app_label = 'support'
        verbose_name = 'HeatmapLayer'
        verbose_name_plural = 'HeatmapLayers'

    def __str__(self):
        return "{}".format(
            self.heatmap_type.name or self.heatmap_type.identifier
        )


# class LayerFilter(models.Model):
#     """
#     Model for LayerFilter Data
#         * Association:
#             * Inherits from :model:`models.Model`
#             * Has many :model:`support.Layer`
#     """

#     default = models.CharField(
#         _("Default value for filters"),
#         max_length=40,
#         blank=True,
#         null=True,
#     )

#     filter_type = models.CharField(
#         _("Filter Type"),
#         max_length=40
#     )

#     label = models.CharField(
#         _("Filter Label"),
#         max_length=40
#     )

#     layers = models.ManyToManyField(
#         Layer,
#         related_name='layer_filters'
#     )

#     class Meta:
#         app_label = 'support'
#         verbose_name = 'LayerFilter'
#         verbose_name_plural = 'LayerFilters'

#     def __str__(self):
#         return "{}: {}".format(self.label, self.filter_type)
