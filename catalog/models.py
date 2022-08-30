from django.db import models

from django.utils.translation import ugettext_lazy as _

class Sattelite (models.Model):
    """Model to store satellite information."""

    identifier = models.CharField(
        _("Identifier"),
        max_length=40,
        unique=True,
    )

    name = models.CharField(
        _("Name sattelite"),
        max_length=255,
        blank=True, # blank=False,
        null=True, # null=False,
    )

    description = models.TextField(
        _("Description"),
        max_length=511,
        blank=True,
        null=True,
    )

    def __str__(self) -> str:
        return self.name or self.identifier
