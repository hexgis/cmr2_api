# python manage.py test catalog.tests.test_models
from urllib import response
from django.test import TestCase

from django.core.management import call_command

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from django.test import Client


class CatalogViewsURLsTests(APITestCase):
    """ Test case MonitoringFiltersTestCase data."""

    @classmethod
    def setUpTestData(cls):
        call_command('loaddata', 'catalog/fixtures/catalog_satellites.yaml', verbosity=0)
        call_command('loaddata', 'catalog/fixtures/catalog_scnes.yaml', verbosity=0)
        cls.url_catalogs = reverse('catalog:catalog-scenes')
        cls.url_satellite = reverse('catalog:satellite-catalog')

    def setUp(self):
        """SetUp for methods."""
        self.client = Client()
 
    def test_xpto1(self):
        response = self.client.get(self.url_satellite)
        # self.assertEqual(response.status_code, 200)
        print(response.json()[0])
        # import pdb; pdb.set_trace()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_url_catalogs(self):
        response = self.client.get(self.url_catalogs)
        # self.assertEqual(response.status_code, 200)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    

class CatalogFiltersViewsTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        call_command('loaddata', 'catalog/fixtures/catalog_satellites.yaml', verbosity=0)
        call_command('loaddata', 'catalog/fixtures/catalog_scnes.yaml', verbosity=0)
        cls.url_catalogs = reverse('catalog:catalog-scenes')
        cls.url_satellite = reverse('catalog:satellite-catalog')
        
    def test_xpto1(self):
        print("------------>>>>>>>>>>-------------")
        self.client.get(self.url_catalogs, {'satellite': 'LC08', 'cloud_cover': 5})
        self.assertEqual(1 + 1, 2)
