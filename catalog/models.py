from django.db import models

from django.utils.translation import ugettext_lazy as _


class Satellite(models.Model):
    """Model to store satellite information."""

    identifier = models.CharField(
        _('Identifier'),
        max_length=40,
        unique=True,
    )

    name = models.CharField(
        _('Satellite name'),
        max_length=255,
        blank=True,
        null=True,
    )

    description = models.TextField(
        _('Description'),
        max_length=511,
        blank=True,
        null=True,
    )

    class Meta:
        """"Meta class for `catalog.Satellite` model."""
        app_label = 'catalog'
        verbose_name = 'Satellite'
        verbose_name_plural = 'Satellites'

    def __str__(self) -> str:
        """Returns `catalog.Satellite` string data.

        Returns:
            str: model data identifier.
        """
        return self.name or self.identifier
