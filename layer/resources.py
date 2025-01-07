from import_export import resources

from . import models


class WmsResource(resources.ModelResource):
    """WmsResource class to set import_id_field and skip configs."""

    class Meta:
        """Meta class for WmsResource."""

        model = models.Wms
        import_id_fields = ('layer', )
        skip_unchaged = True
        report_skipped = False


class TmsResource(resources.ModelResource):
    """TmsResource class to set import_id_field and skip configs."""

    class Meta:
        """Meta class for TmsResource."""

        model = models.Tms
        import_id_fields = ('layer', )
        skip_unchaged = True
        report_skipped = False
