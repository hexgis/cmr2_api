from django.test import TestCase

from django.core.management import call_command

from catalog import models


class SceneTest(TestCase):
    """Test case `catalog.Scene` model"""

    @classmethod
    def setUpTestData(cls):
        """Class variables using dumpdata fixtures file"""
        call_command('loaddata',
            'catalog/fixtures/catalog_satellites.yaml',
            verbosity=0)
        call_command('loaddata',
            'catalog/fixtures/catalog_scnes.yaml',
            verbosity=0)

    def test_objects_created(self):
        """Test if object Scene is created."""
        self.assertTrue(models.Scene.objects.exists())

    def test_object_output_name_is_image(self):
        """Test the model output is named Catalog Image"""
        catalog_image = models.Scene.objects.first()
        expected_object_name = f'{catalog_image.image}'

        self.assertEqual(expected_object_name, str(catalog_image))

    def test_related_catalog_satellite_exists(self):
        """Test if related catalog satellite exists"""
        catalog_image = models.Scene.objects.values_list(
            'sat', 'sat_id__name')[:1].get()
        satellite = models.Satellite.objects.get(id=catalog_image[0])

        self.assertEqual(catalog_image[1],str(satellite))


class SatelliteTest(TestCase):
    """Test case `catalog.Satellite` model"""

    @classmethod
    def setUpTestData(cls):
        """Class variables dumpdata using fixtures file"""
        call_command(
            'loaddata',
            'catalog/fixtures/catalog_satellites.yaml',
            verbosity=0)

    def test_object_created(self):
        """Test if object Satellite is created."""
        self.assertTrue(models.Satellite.objects.exists())

    def test_object_model_output_is_name_or_identifier(self):
        """Test the model output is named Satellite Name or Identifier."""
        satellite = models.Satellite.objects.first()
        expected_object_name = [satellite.name, satellite.identifier]

        self.assertIn(str(satellite), expected_object_name)
