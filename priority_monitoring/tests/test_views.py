# from inspect import Parameter
# from time import strptime
# from urllib import response
from rest_framework.test import APITestCase
from django.test import Client
from rest_framework import status
from datetime import datetime

from django.core.management import call_command
from django.urls import reverse

from priority_monitoring import models


class PiorirityConsolidatedViewsTests(APITestCase):
    """Test case PiorirityConsolidatedViewTests data."""

    def get_requered_filters_parameters(self):
        """Creating parameters requered applied to filters."""
        parameter = {
            'start_date': '2021-07-28',
            'end_date': '2021-12-15',
            'pk_detail': 13
        }

        return parameter

    @classmethod
    def setUpTestData(cls):
        """Class variables using dumpdata fixtures file end URLs."""
        cls.parameters = cls.get_requered_filters_parameters(cls)

        cls.url_pioririty_consolidated = reverse(
            'priority_monitoring:priority-consolidated'
        )
        cls.url_pioririty_consolidated_priorities = reverse(
            'priority_monitoring:priority-consolidated-priorities'
        )
        cls.url_pioririty_consolidated_detail = reverse(
            'priority_monitoring:priority-consolidated-detail',
            kwargs={'pk': cls.parameters['pk_detail']}
        )
        cls.url_pioririty_consolidated_stats = reverse(
            'priority_monitoring:priority-consolidated-stats'
        )
        cls.url_pioririty_consolidated_table = reverse(
            'priority_monitoring:priority-consolidated-table'
        )

    def SetUp(self):
        """SetUp for methods."""
        self.client = Client()

    def test_url_pioririty_consolidated(self):
        """Test url pioririty consolidated."""
        res = self.client.get(self.url_pioririty_consolidated, {'start_date': self.parameters['start_date'],
                                                                     'end_date': self.parameters['end_date']})

        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_url_pioririty_consolidated_priorities(self):
        """Test url pioririty consolidated priorities."""
        res = self.client.get(self.url_pioririty_consolidated_priorities)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_url_pioririty_consolidated_detail(self):
        """Test url pioririty consolidated detail."""
        res = self.client.get(self.url_pioririty_consolidated_detail)

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_url_pioririty_consolidated_stats(self):
        """Test url pioririty consolidated stats."""
        res = self.client.get(self.url_pioririty_consolidated_stats, {'start_date': self.parameters['start_date'],
                                                                           'end_date': self.parameters['end_date']})

        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_url_pioririty_consolidated_table(self):
        """Test url pioririty consolidated table."""
        res = self.client.get(self.url_pioririty_consolidated_table, {'start_date': self.parameters['start_date'],
                                                                           'end_date': self.parameters['end_date']})

        self.assertEqual(res.status_code, status.HTTP_200_OK)


class PiorirityConsolidatedFiltersViewsTests(APITestCase):
    """Test case PiorirityConsolidatedFiltersViewsTests data."""

    def get_filters_parameters(self):
        """Creating parameters applied to filters."""
        parameter = {
            'co_cr': 30202001920,
            'co_funai': 23001,
            'stage': 'CR',
            'start_date': '2021-07-28',
            'end_date': '2021-12-15',
            'priority': 'Baixa',
            'pk_detail': 13
        }

        return parameter

    @classmethod
    def setUpTestData(cls):
        """Class variables using dumpdata fixtures file end URLs."""
        cls.parameters = cls.get_filters_parameters(cls)

        call_command(
            'loaddata',
            'priority_monitoring/fixtures/priority_consolidated.yaml',
            verbosity=0)

        cls.url_pioririty_consolidated_detail = reverse(
            'priority_monitoring:priority-consolidated-detail',
            kwargs={'pk': cls.parameters['pk_detail']}
        )
        cls.url_pioririty_consolidated_table = reverse(
            'priority_monitoring:priority-consolidated-table'
        )

    def setUp(self):
        """SetUp for methods."""
        self.client = Client()

        self.queryset_valid = models.PriorityConsolidated.objects.filter(
            co_cr=self.parameters['co_cr'],
            co_funai=self.parameters['co_funai'],
            no_estagio=self.parameters['stage'],
            dt_t_um__gte=self.parameters['start_date'],
            dt_t_um__lte=self.parameters['end_date'],
            prioridade=self.parameters['priority']
        )
        self.request_valid = self.client.get(self.url_pioririty_consolidated_table, {
            'co_cr': self.parameters['co_cr'],
            'co_funai': self.parameters['co_funai'],
            'stage': self.parameters['stage'],
            'start_date': self.parameters['start_date'],
            'end_date': self.parameters['end_date'],
            'priority': self.parameters['priority']
        })
        self.request_error = self.client.get(self.url_pioririty_consolidated_table, {
            'co_cr': "Kayapó",
            'start_date': self.parameters['start_date'],
            'end_date': self.parameters['end_date']
        })

    def test_valid_parameters(self):
        """Test valid URL parameters."""
        res = self.request_valid

        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_invalid_parameters(self):
        """Test invalid URL parameters."""
        res = self.request_error

        self.assertTrue(status.is_client_error(res.status_code))

    def test_objects_queryset_created(self):
        """Test if object queryset is created."""
        qs = self.queryset_valid

        self.assertTrue(qs.exists())

    def test_request_with_filters_is_valid(self):
        """Testing if the request with filters is valid."""
        res = self.request_valid.json()
        date_format = "%Y-%m-%d"

        for i in range(len(res)):
            self.assertEqual(res[i]['co_cr'], self.parameters['co_cr'])
            self.assertEqual(res[i]['co_funai'], self.parameters['co_funai'])
            self.assertEqual(res[i]['no_estagio'], self.parameters['stage'])
            self.assertEqual(res[i]['prioridade'], self.parameters['priority'])
            self.assertTrue(
                datetime.strptime(self.parameters['start_date'], date_format) <=
                datetime.strptime(res[i]['dt_t_um'], date_format) <=
                datetime.strptime(self.parameters['end_date'], date_format)
            )

    def test_request_filter_is_equals_len_queryset_filter(self):
        """test record amount of request is iqual to queyrsaf."""
        res = self.request_valid.json()
        qs = self.queryset_valid

        self.assertEqual(len(res), qs.count())

    def test_inbbox_filter(self):
        # TODO: create methodology for inbbox tests
        pass
