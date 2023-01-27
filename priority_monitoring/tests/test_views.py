from urllib import response
from rest_framework.test import APITestCase
from django.test import Client
from rest_framework import status
from datetime import datetime

from django.core.management import call_command
from django.urls import reverse

from priority_monitoring import models


class PiorirityConsolidatedViewsTests(APITestCase):
    """Test case PiorirityConsolidatedViewTests data."""

    @classmethod
    def setUpTestData(cls):
        """Class variables using dumpdata fixtures file end URLs."""
        # call_command('loaddata', 'priority_monitoring/fixtures/priority_consolidated.yaml', verbosity=0)
        cls.url_pioririty_consolidated = reverse('priority_monitoring:priority-consolidated')
        cls.url_pioririty_consolidated_priorities = reverse('priority_monitoring:priority-consolidated-priorities')
        cls.url_pioririty_consolidated_detail = reverse('priority_monitoring:priority-consolidated-detail')
        cls.url_pioririty_consolidated_stats = reverse('priority_monitoring:priority-consolidated-stats')
        cls.url_pioririty_consolidated_table = reverse('priority_monitoring:priority-consolidated-table')
    
    def SetUp (self):
        """SetUp for methods."""
        self.client = Client()

    def test_url_pioririty_consolidated(self):
        response = self.client.get(self.url_pioririty_consolidated)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_url_pioririty_consolidated_priorities(self):
        response = self.client.get(self.url_pioririty_consolidated_priorities)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_url_pioririty_consolidated_detail(self):
        response = self.client.get(self.url_pioririty_consolidated_detail)
        #add pk
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_url_pioririty_consolidated_stats(self):
        response = self.client.get(self.url_pioririty_consolidated_stats)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_url_pioririty_consolidated_table(self):
        response = self.client.get(self.url_pioririty_consolidated_table)

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class PiorirityConsolidatedFiltersViewsTests(APITestCase):
    """Test case PiorirityConsolidatedFiltersViewsTests data."""
    
    def get_filters_parameters(self):
        """Creating parameters applied to filters."""
        parameter = {
            'co_cr': 30202001920,
            'co_funai': 23001,
            'stage': 'CR',
            'start_date':'2021-12-15',
            'end_date':'2021-07-28',
            'priority': 'Baixa',
        }

        return parameter

    @classmethod
    def setUpTestData(cls):
        call_command(
            'loaddata',
            'priority_monitoring/fixtures/priority_consolidated.yaml',
            verbosity=0)
        cls.url_pioririty_consolidated = reverse('priority_monitoring:priority-consolidated')
        # cls.url_pioririty_consolidated_priorities = reverse('priority_monitoring:priority-consolidated-priorities')
        # cls.url_pioririty_consolidated_detail = reverse('priority_monitoring:priority-consolidated-detail')
        # cls.url_pioririty_consolidated_stats = reverse('priority_monitoring:priority-consolidated-stats')
        # cls.url_pioririty_consolidated_table = reverse('priority_monitoring:priority-consolidated-table')
    
    def setUp(self):
        self.client = Client()
        self.parameters = self.get_filters_parameters()

        self.queryset_valid = models.PriorityConsolidated.objects.filter(
            co_cr=self.parameters['co_cr'],
            co_funai=self.parameters['co_funai'],
            no_estagio=self.parameters['stage'],
            dt_t_um__gte=self.parameters['start_date'],
            dt_t_um__lte=self.parameters['end_date'],
            prioridade=self.parameters['priority']
        )
        self.request_valid = self.client.get(self.url_pioririty_consolidated, {
            'co_cr':self.parameters['co_cr'],
            'co_funai':self.parameters['co_funai'],
            'stage':self.parameters['stage'],
            'start_date':self.parameters['start_date'],
            'end_date':self.parameters['end_date'],
            'priority':self.parameters['priority']
        })
        self.request_error = self.client.get(self.url_pioririty_consolidated, {
            'co_cr':"Kayapó"
            #adicionar outros
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
        qs = self.queryset_valid

        self.assertTrue(qs.exists())

