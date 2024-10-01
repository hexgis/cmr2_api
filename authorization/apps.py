import django.apps

from authorization import signals_permissions
from django.db.models.signals import post_migrate


class AuthorizationConfig(django.apps.AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'authorization'

    def ready(self):
        """Runs activity ever a migration is performed."""
        signals_permissions
        post_migrate.connect(signals_permissions.create_cmr_access_permissions, sender=self)
