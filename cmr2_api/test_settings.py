from django.test.runner import DiscoverRunner
from django.conf import settings
import sys
from django.apps import apps


if 'test' in sys.argv or 'test_coverage' in sys.argv:  # Covers regular testing and django-coverage
    settings.DATABASE_ROUTERS = {}


class DisableMigrations(object):
    def __contains__(self, item):
        return True

    def __getitem__(self, item):
        return "notmigrations"


class ManagedModelTestRunner(DiscoverRunner):
    """
    Test runner that automatically makes all unmanaged models in your Django
    project managed for the duration of the test run, so that one doesn't need
    to execute the SQL manually to create them.
    """

    def setup_test_environment(self, *args, **kwargs): 
            """Creating test database for alias 'default' used in unit tests of unmanaged models."""

            get_models = apps.get_models 
            self.unmanaged_models = [m for m in get_models() if not m._meta.managed and m._meta.app_label in settings.INSTALLED_APPS] #3

            for m in self.unmanaged_models:
                m._meta.managed = True 
                m.objects.model._meta.db_table = m.objects.model._meta.app_label + '_' + m.objects.model._meta.model_name 

            super(ManagedModelTestRunner, self).setup_test_environment(*args, **kwargs)

    def teardown_test_environment(self, *args, **kwargs):
        """Destroying test database for alias 'default' used in unit tests of unmanaged models."""

        super(ManagedModelTestRunner, self).teardown_test_environment(*args, **kwargs)

        for m in self.unmanaged_models:
            m._meta.managed = False
