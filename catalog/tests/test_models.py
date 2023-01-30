from django.test import TestCase

from django.core.management import call_command

from catalog import models


class CatalogsTest(TestCase):
    """Test case `catalog.Catalogs` model"""

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
        """Test if object Catalogs is created."""
        self.assertTrue(models.Catalogs.objects.exists())

    def test_object_output_name_is_image(self):
        """Test the model output is named Catalog Image"""
        catalog_image = models.Catalogs.objects.first()
        expected_object_name = f'{catalog_image.image}'

        self.assertEqual(expected_object_name, str(catalog_image))

    def test_related_catalog_satellite_exists(self):
        """Test if related catalog satellite exists"""
        catalog_image = models.Catalogs.objects.values_list(
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
