from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.postgres.fields import ArrayField
from django.conf import settings


class LayerPermission(models.Model):
    """Model to store layer permission.

    * Association:
        * Has many :model:`layer.LayerNew`
    """

    name = models.CharField(max_length=50)

    description = models.CharField(max_length=255)

    layers = models.ManyToManyField(
        'layer.Layer',
        related_name='layer_permissions',
        blank=True
    )

    def __str__(self):
        """Model class string.

        Returns:
            str: short description of LayerPermission model.
        """

        return f'{self.name} | {self.description}'

    class Meta:
        """Meta class for LayerPermission model."""

        app_label = 'permission'


class ComponentPermission(models.Model):
    """Model to store component permission."""

    name = models.CharField(max_length=50)

    description = models.CharField(max_length=255)

    components = ArrayField(
        models.CharField(
            max_length=20,
            choices=settings.COMPONENT_LIST
        ),
        blank=True
    )

    def __str__(self):
        """Model class string.

        Returns:
            str: short description of ComponentPermission model.
        """

        return f'{self.name} | {self.description}'

    class Meta:
        """Meta class for ComponentPermission model."""

        app_label = 'permission'
