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
        verbose_name_plural = 'Permissions List'
        constraints = [
            models.UniqueConstraint(fields=['group_id', 'permission_layer_id'], name='unique_permission_per_group_layer')
        ]

    def clean(self):
        super().clean()
        if self.is_layer:
            if self.permission or self.permission_name:
                raise ValidationError('Permission and permission_name should be null if is_layer is False.')
        else:
            if self.permission_layer_id or self.permission_layer_name:
                raise ValidationError('Permission_layer_id and permission_layer_name should be null if is_layer is True.')