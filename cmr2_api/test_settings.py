import sys
from django.test.runner import DiscoverRunner

from django.conf import settings
from django.apps import apps


if 'test' in sys.argv or 'test_coverage' in sys.argv:  # Covers regular testing and django-coverage
    settings.DATABASE_ROUTERS = {}


class ManagedModelTestRunner(DiscoverRunner):
    """
    United test runner that automatically makes all unmanaged models in the
    database for alias 'test_default_db', the Django project's test database.
    """

    def setup_test_environment(self, *args, **kwargs): 
            """Creating test database for alias 'default' used in unit tests
            of unmanaged models.
            """

            apps_not_execut_united_test =['monitoring','catalog','priority_monitoring']
            get_models = apps.get_models

            self.unmanaged_models = [
                m for m in get_models()
                if not m._meta.managed
                and m._meta.app_label in settings.INSTALLED_APPS
                and not m._meta.app_label in apps_not_execut_united_test
            ]

            for m in self.unmanaged_models:
                m._meta.managed = True
                m.objects.model._meta.db_table = m.objects.model._meta.app_label + '_' + m.objects.model._meta.model_name 

            super(ManagedModelTestRunner, self).setup_test_environment(*args, **kwargs)

    def teardown_test_environment(self, *args, **kwargs):
        """Destroying test database for alias 'default' used in unit tests of
        unmanaged models.
        """

        super(ManagedModelTestRunner, self).teardown_test_environment(*args, **kwargs)

        for m in self.unmanaged_models:
            m._meta.managed = False
