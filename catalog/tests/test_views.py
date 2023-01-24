# python manage.py test catalog.tests.test_views
from urllib import response
from django.test import TestCase

from django.core.management import call_command

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from django.test import Client
from catalog import models


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
 
    def test_url_satellite(self):
        response = self.client.get(self.url_satellite)
        # self.assertEqual(response.status_code, 200)
        # print(response.json()[0], "Primeira class")
        # import pdb; pdb.set_trace()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_url_catalogs(self):
        response = self.client.get(self.url_catalogs)
        # self.assertEqual(response.status_code, 200)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    

class CatalogFiltersViewsTests(APITestCase):
    """"""
    def get_filters_parameters(self):
        parameter = {
            'satellite': 'LC08',
            'cloud_cover': 99,
            'start_date':'2018-06-14',
            'end_date':'2021-10-14',
        }

        return parameter

    @classmethod
    def setUpTestData(cls):
        call_command('loaddata', 'catalog/fixtures/catalog_satellites.yaml', verbosity=0)
        call_command('loaddata', 'catalog/fixtures/catalog_scnes.yaml', verbosity=0)
        cls.url_catalogs = reverse('catalog:catalog-scenes')
        cls.url_satellite = reverse('catalog:satellite-catalog')

    def setUp(self):
        self.client = Client()
        self.parameter = self.get_filters_parameters()
        self.request_valid = self.client.get(self.url_catalogs, {
            'satellite':self.parameter['satellite'],
            'cloud_cover':self.parameter['cloud_cover'],
            'start_date':self.parameter['start_date'],
            'end_date':self.parameter['end_date']
        })
        self.queryset_valid = models.Catalogs.objects.filter(
            sat_id__identifier__exact=self.parameter['satellite'],
            cloud_cover__lte=self.parameter['cloud_cover'],
            date__gte=self.parameter['start_date'],
            date__lte=self.parameter['end_date']
        )
        self.request_error = self.client.get(self.url_catalogs, {
            'satellite': 'LC08',
            'cloud_cover': 5,
            'start_date': '2021-01-066'
        })

    def test_request_with_filters_is_valid(self):
        print("------------>>>>>>>>>>-------------")
        import pdb; pdb.set_trace()
        # self.client.get(self.url_catalogs, {'satellite': 'LC08', 'cloud_cover': 5})
        response = self.request_valid
        for i in range(len(response.json())): 
            response.json()[i]['objectid']
            se todos os valores são iguais a = 'satellite': 'LC08',
            #TODO: 
            self.assertEquals(response.json()[i]['sat'], 2)
            se todos os valores são maiores ou iguais a = 'cloud_cover': 99,
            se todos os valores são menores ou iguas a = 'start_date':'2018-06-14',
            se todos os valores são maiores ou iguais a = 'end_date':'2021-10-14',
       
        self.assertEqual(1+3, 5)
        # self.assertEqual(request_valid.status_code, status.HTTP_200_OK)

    def test_request_filter_is_equals_len_queryset_filter(self):
        response = self.request_valid.json()
        qs = self.queryset_valid

        self.assertEqual(len(response), qs.count())
        # len(self.request_valid.json(),self.queryset_valid.count())

    def test_invalid_parameter(self):
        response = self.request_error

        self.assertTrue(status.is_client_error(response.status_code))
