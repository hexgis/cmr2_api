from rest_framework.test import APITestCase

from django.core.management import call_command

from land_use import models


class LandUseTITests(APITestCase):
    """Test case `models.land_use.LandUseTI` model.

    Args:
        APITestCase (class 'rest_framework.test.APITestCase'): Includes a few
            helper classes that extend Django's existing test framework.
    """

    @classmethod
    def setUpTestData(cls):
        """Class variables using dumpdata fixtures file."""

        call_command(
            'loaddata',
            'land_use/fixtures/land_use_ti.yaml',
            verbosity=0)

    def test_objects_landuseti_created(self):
        """Test if object LandUseTI is created."""

        self.assertTrue(models.LandUseTI.objects.exists())


class LandUseClassesTests(APITestCase):
    """Test case `models.land_use.LandUseClasses` model.

    Args:
        APITestCase (class 'rest_framework.test.APITestCase'): Includes a few
            helper classes that extend Django's existing test framework.
    """

    @classmethod
    def setUpTestData(cls):
        """Class variables using dumpdata fixtures file."""

        call_command(
            'loaddata',
            'land_use/fixtures/land_use_classes.yaml',
            verbosity=0)

    def test_objects_landuseclasses_created(self):
        """Test if object LandUseClasses is created."""

        self.assertTrue(models.LandUseClasses.objects.exists())

#TODO: Create test_views tests.
