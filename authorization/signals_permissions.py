import django.apps
from django.contrib import contenttypes, auth


def create_cmr_access_permissions(sender, **kwargs):
    """Create action access. Adding permission in all installed app models."""
    for model in django.apps.apps.get_models():
        auth.models.Permission.objects.get_or_create(
            codename = f'access_{model.__name__}'.lower(),
            name = f'Can access {model.__name__} in CMR',
            content_type = contenttypes.models.ContentType.objects.get_for_model(model),)
