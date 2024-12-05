from django.contrib.gis.db import models
from support import models as supportmodel
from django.core.exceptions import ValidationError


class PermissionsList(models.Model):
    permission_layer_id = models.OneToOneField(
        supportmodel.Layer,
        on_delete=models.DO_NOTHING
    )
    permission_layer_name = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    class Meta:
        app_label = 'authorization'
        verbose_name = 'Permission'
