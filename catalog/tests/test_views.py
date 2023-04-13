from rest_framework.test import APITestCase
from django.test import Client
from rest_framework import status
from datetime import datetime

from django.core.management import call_command
from django.urls import reverse

from catalog import models


class CatalogViewsURLsTests(APITestCase):
    """Test case CatalogViewsURLsTests data."""

    @classmethod
    def setUpTestData(cls):
        """Class variables using dumpdata fixtures file end URLs."""
        cls.url_Scene = reverse('catalog:catalog-scenes')
        cls.url_satellite = reverse('catalog:satellite-catalog')

    def setUp(self):
        """SetUp for methods."""
        self.client = Client()

    def test_url_satellite(self):
        """Test valid URL satellite-scenes."""
        response = self.client.get(self.url_satellite)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_url_Scene(self):
        """Test valid URL catalog-scenes."""
        response = self.client.get(self.url_Scene)

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class CatalogFiltersViewsTests(APITestCase):
    """ Test case CatalogFiltersViewsTests data."""

    def get_filters_parameters(self):
        """Creating parameters applied to filters."""
        parameter = {
            'satellite': 'LC08',
            'cloud_cover': 99,
            'start_date':'2018-06-14',
            'end_date':'2021-10-14',
        }

        return parameter

    @classmethod
    def setUpTestData(cls):
        """Class variables using dumpdata fixtures file end URLs."""
        call_command(
            'loaddata',
            'catalog/fixtures/catalog_satellites.yaml',
            verbosity=0)
        call_command(
            'loaddata',
            'catalog/fixtures/catalog_scnes.yaml',
            verbosity=0)
        cls.url_Scene = reverse('catalog:catalog-scenes')

    def setUp(self):
        """SetUp for methods, generate queryset and requests."""
        self.client = Client()
        self.parameter = self.get_filters_parameters()
        self.request_valid = self.client.get(self.url_Scene, {
            'satellite':self.parameter['satellite'],
            'cloud_cover':self.parameter['cloud_cover'],
            'start_date':self.parameter['start_date'],
            'end_date':self.parameter['end_date']
        })
        self.queryset_valid = models.Scene.objects.filter(
            sat_id__identifier__exact=self.parameter['satellite'],
            cloud_cover__lte=self.parameter['cloud_cover'],
            date__gte=self.parameter['start_date'],
            date__lte=self.parameter['end_date']
        )
        self.request_error = self.client.get(self.url_Scene, {
            'satellite': 'LC08',
            'cloud_cover': 5,
            'start_date': '2021-01-066'
        })

    def test_valid_parameters(self):
        """Test valid URL parameters on catalog-scenes."""
        response = self.request_valid

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_parameters(self):
        """Test invalid URL parameters on catalog-scenes."""
        response = self.request_error

        self.assertTrue(status.is_client_error(response.status_code))

    def test_objects_queryset_created(self):
        """Test if object queryset is created."""
        self.assertTrue(self.queryset_valid.exists())

    def test_request_with_filters_is_valid(self):
        """Testing if the request with filters is valid."""
        response = self.request_valid
        date_format = "%Y-%m-%d"
        for i in range(len(response.json())):
            #TODO: Validar regra de negocio para saber se irá atribuir o sat
            # identify ao serializador
            self.assertEquals(response.json()[i]['sat'], 2)
            self.assertTrue(response.json()[i]['cloud_cover'] <= 
                            self.parameter['cloud_cover'])
            self.assertTrue(
                datetime.strptime(self.parameter['start_date'], date_format) <=
                datetime.strptime(response.json()[i]['date'], date_format) <=
                datetime.strptime(self.parameter['end_date'], date_format))

    def test_request_filter_is_equals_len_queryset_filter(self):
        """test record amount of request is iqual to queyrsaf."""
        response = self.request_valid.json()
        qs = self.queryset_valid

        self.assertEqual(len(response), qs.count())
