import os

from django.utils.translation import ugettext_lazy as _
from django.db import transaction
from django.core.exceptions import ValidationError


@transaction.atomic
def validate_json_extension(data: str) -> None:
    """Validation to ensure the file has a geojson extension.

    Raises:
        ValidationError: Unsupported extension.
    """

    enabled_extensions = ['.json', '.geojson']

    ext = os.path.splitext(data.name)[1]

    if ext.lower() not in enabled_extensions:
        raise ValidationError(
            _('Unsupported extension. Please, upload a geojson file.')
        )
