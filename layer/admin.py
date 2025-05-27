import base64

from django.contrib.gis import admin
from django.db.models import JSONField, When, Value, Case
from django.utils.html import format_html

from leaflet.admin import LeafletGeoAdminMixin
from import_export.admin import ImportExportActionModelAdmin as import_export
from django_json_widget.widgets import JSONEditorWidget

from layer import resources, models
from permission.mixins import Auth


class GeoserverAdmin(import_export):
    """GeoserverAdmin class to `models.Geoserver` data."""

    list_display = (
        'id',
        'name',
        'wms_url',
        'preview_url',
    )

    search_fields = list_display


class GroupAdmin(import_export):
    """GroupAdmin class to `models.Group` data."""

    list_display = (
        'id',
        'name',
        'order',
    )

    search_fields = list_display


class LayerAdmin(LeafletGeoAdminMixin, import_export):
    """LayerAdmin class to `models.Layer` data."""

    actions = ['make_downloadable', 'remove_downloadable']

    @admin.action(description='Mark layer as downloadable')
    def make_downloadable(self, request, queryset):
        """Mark `Layer` as downladable.

        Args:
            request (Request): user request.
            queryset (Queryset): Django model queryset.
        """

        queryset.update(is_downloadable=True)
        self.message_user(
            request, f'{queryset.count()} marked as downloadable'
        )

    @admin.action(description='Unmark layer as downloadable')
    def remove_downloadable(self, request, queryset):
        """Remove downloadable attribute from `Layer`.

        Args:
            request (Request): user request.
            queryset (Queryset): Django model queryset.
        """

        queryset.update(is_downloadable=False)
        self.message_user(
            request, f'{queryset.count()} unmarked as downloadable'
        )

    list_display = (
        'id',
        'name',
        'order',
        'active_on_init',
        'group',
        'is_downloadable',
        'is_public',
    )

    search_fields = (
        'name',
        'group__name',
    )

    list_filter = (
        'group',
        'is_public',
    )


class WmsAdmin(LeafletGeoAdminMixin, import_export):
    """WmsAdmin class to `models.Wms` data."""

    actions = [
        'update_thumbnail_blob',
        'update_bbox',
        'toggle_has_sublayers',
        'toggle_has_opacity',
        'toggle_has_metadata'
    ]

    @admin.action(description='Update thumbnail blob')
    def update_thumbnail_blob(self, request, queryset):
        """Update thumbnail for `WmsLayer` according to selected type.

        Args:
            request (Request): user request.
            queryset (Queryset): Django model queryset.
        """

        for layer in queryset:
            layer.get_thumbnail_blob()
            layer.save()

        self.message_user(
            request, f'{queryset.count()} thumbnail(s) updated.'
        )

    @admin.action(description='Update layer bbox')
    def update_bbox(self, request, queryset):
        """Update bbox for `WmsLayer`.

        Args:
            request (Request): user request.
            queryset (Queryset): Django model queryset.
        """

        for layer in queryset:
            layer.get_bbox()
            layer.save()

        self.message_user(request, f'{queryset.count()} bbox updated.')

    @admin.action(description='Toggle has_sublayer')
    def toggle_has_sublayers(self, request, queryset):
        """Update has_sublayer attribute for `WmsLayer`.

        Args:
            request (Request): user request.
            queryset (Queryset): Django model queryset.
        """

        queryset.update(has_sublayers=Case(
            When(has_sublayers=True, then=Value(False)),
            default=Value(True),
        ))

        self.message_user(
            request, f'{queryset.count()} has_sublayer attr toggled.'
        )

    @admin.action(description='Toggle has_metadata')
    def toggle_has_metadata(self, request, queryset):
        """Update has_metadata attribute for `WmsLayer`.

        Args:
            request (Request): user request.
            queryset (Queryset): Django model queryset.
        """

        queryset.update(has_metadata=Case(
            When(has_metadata=True, then=Value(False)),
            default=Value(True),
        ))

        self.message_user(
            request, f'{queryset.count()} has_metadata attr toggled.'
        )

    @admin.action(description='Toggle has_opacity')
    def toggle_has_opacity(self, request, queryset):
        """Toggle has_opacity attribute for `WmsLayer`.

        Args:
            request (Request): user request.
            queryset (Queryset): Django model queryset.
        """

        queryset.update(has_opacity=Case(
            When(has_opacity=True, then=Value(False)),
            default=Value(True),
        ))

        self.message_user(
            request, f'{queryset.count()} has_opacity attr toggled.'
        )

    def thumbnail_image(self, instance: models.Wms) -> str:
        """Get thumbnail image in html format.

        Args:
            instance (models.Wms): Wms model data.

        Returns:
            models.Wms: string info.
        """

        if instance.thumbnail_blob:
            img = base64.b64encode(instance.thumbnail_blob).decode('UTF-8')
            return format_html(
                f'<img width="40" height="40" src=data:image/png;base64,{img}>'
            )
        else:
            return None

    def geoserver_layername(self, instance: models.Wms) -> str:
        """Get thumbnail image in html format.

        Args:
            instance (models.Wms): Wms model data.

        Returns:
            models.Wms: string info.
        """

        return f'{instance.geoserver_layer_namespace}:{instance.geoserver_layer_name}'

    search_fields = (
        'name',
        'group__name',
        'geoserver_layer_name',
        'geoserver_layer_namespace',
    )

    list_filter = (
        'group',
        'geoserver',
        'has_preview',
        'has_detail',
        'has_sublayers',
    )

    list_display = (
        'id',
        'name',
        'geoserver_layername',
        'has_sublayers',
        'has_opacity',
        'has_metadata',
        'preview_type',
        'thumbnail_image',
    )

    readonly_fields = ('thumbnail_image', )


class TmsAdmin(LeafletGeoAdminMixin, import_export):
    """TmsAdmin class to `models.Tms` data."""

    resource_class = resources.TmsResource

    list_display = (
        'name',
        'group',
        'url',
        'max_native_zoom',
        'is_tms',
    )

    list_filter = (
        'group',
        'is_tms',
    )


class FilterAdmin(import_export):
    """LayerFilterAdmin class to `models.Filter` data."""

    list_display = (
        'label',
        'default',
        'type',
        'alias',
    )

    list_filter = (
        'type',
        'alias',
    )


class BasemapAdmin(import_export):
    """LayerFilterAdmin class to `models.Filter` data."""

    list_display = (
        'id',
        'url',
        'label',
        'tag',
        'attribution',
    )

    list_filter = (
        'label',
        'tag',
    )


class VectorAdmin(LeafletGeoAdminMixin, import_export):
    """VectorAdmin class to `models.Vector` data."""

    def thumbnail_image(self, instance: models.Vector) -> str:
        """Get thumbnail image in html format.

        Args:
            instance (models.Vector): Vector model data.

        Returns:
            models.Vector: string info.
        """

        if instance.thumbnail_blob:
            img = base64.b64encode(instance.thumbnail_blob).decode('UTF-8')
            return format_html(
                f'<img src=data:image/png;base64,{img} height=40>'
            )
        else:
            return None

    list_display = (
        'name',
        'type',
        'group',
        'thumbnail_image'
    )

    list_filter = (
        'group',
        'type',

    )


class VectorGeometryAdmin(LeafletGeoAdminMixin, import_export,):
    """VectorGeometryAdmin class to models.VectorGeometryAdmin data."""

    formfield_overrides = {
        JSONField: {'widget': JSONEditorWidget},
    }

    list_display = (
        'id',
        'vector_uploaded',
        'properties',
    )

    list_filter = (
        'vector_uploaded__group',
        'vector_uploaded'
    )


class BookmarkAdmin(
    LeafletGeoAdminMixin,
    import_export,
    admin.GeoModelAdmin
):
    """BookmarkAdmin admin model data."""

    list_display = (
        'id',
        'user',
        'user_id',
        'name',
    )

    fields = (
        'user',
        'name',
        'layers',
        'bbox',
        'images',
    )

    search_fields = ('user', 'name',)

    list_filter = ('user', )


admin.site.register(models.Vector, VectorAdmin)
admin.site.register(models.Geoserver, GeoserverAdmin)
admin.site.register(models.Group, GroupAdmin)
admin.site.register(models.Layer, LayerAdmin)
admin.site.register(models.Wms, WmsAdmin)
admin.site.register(models.Tms, TmsAdmin)
admin.site.register(models.Filter, FilterAdmin)
admin.site.register(models.Basemap, BasemapAdmin)
admin.site.register(models.VectorGeometry,
                    VectorGeometryAdmin)
