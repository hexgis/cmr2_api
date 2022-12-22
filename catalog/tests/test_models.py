from django.test import TestCase

from catalog import models
from django.core.management import call_command


class CatalogsTest(TestCase):
    """"""
    @classmethod
    def setUpTestData(cls):
        """"""
        call_command('loaddata', 'catalog/fixtures/catalog_satellites.yaml', verbosity=0)
        call_command('loaddata', 'catalog/fixtures/catalog_scnes.yaml', verbosity=0)

    def test_objects_created(self):
        """"""
        self.assertTrue(models.Catalogs.objects.exists())

    def test_object_name_is_image(self):
        """"""
        catalog_image = models.Catalogs.objects.first()
        expected_object_name = f'{catalog_image.image}'

        self.assertEqual(expected_object_name, str(catalog_image))
    
    def test_related_catalog_satellite_exists(self):
        """"""
        catalog_image = models.Catalogs.objects.values_list('sat', 'sat_id__name')[:1].get()
        satellite = models.Satellite.objects.get(id=catalog_image[0])

        self.assertEqual(catalog_image[1],str(satellite))


class SatelliteTest(TestCase):
    """"""

    @classmethod
    def setUpTestData(cls):
        call_command('loaddata', 'catalog/fixtures/catalog_satellites.yaml', verbosity=0)

    def test_object_created(self):
        """"""
        self.assertFalse(models.Satellite.objects.exists())

    def test_object_model_exit_is_name_or_identifier(self):
        """"""
        satellite = models.Satellite.objects.first()
        expected_object_name = [satellite.name, satellite.identifier]

        self.assertIn(str(satellite), expected_object_name)
