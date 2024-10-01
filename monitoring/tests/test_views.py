from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.test import TestCase

from django.core.management import call_command
from monitoring import models


class MonitoringFiltersTestCase(TestCase):
    """ Test case MonitoringFiltersTestCase data."""

    @classmethod
    def setUpTestData(cls):
        """SetUp for Class."""
        call_command(
            'loaddata', 'monitoring/fixtures/monitoring_priority_consolidated.yaml', verbosity=0)
        cls.url_base = reverse('monitoring:monitoring')
        # cls.url_detail = reverse('monitoring:monitoring-detail')
        cls.url_map_stats = reverse('monitoring:monitoring-map-stats')
        cls.url_classes = reverse('monitoring:monitoring-classes')
        cls.url_table = reverse('monitoring:monitoring-table')
        cls.url_table_stats = reverse('monitoring:monitoring-table-stats')

    def setUp(self):
        """SetUp for methods."""
        self.client = APIClient()
        response = self.client.get(self.url_table)
        self.co_cr = response.json()[0]['co_cr']
        self.co_funai = response.json()[0]['co_funai']
        self.no_estagio = response.json()[0]['no_estagio']
        self.queryset = models.MonitoringConsolidated.objects.all()

    def tearDown(self):
        """TearDown for methods."""
        pass

    def test_url_source(self):
        """
        Verify source endpoint

        tests:
        - If Url is ok
        """

        response = self.client.get(self.url_base)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_monitoring_map_stats(self):
        """
        Verify monitoring map stats endpoint

        tests:
        - If Url is ok
        """
        response = self.client.get(self.url_map_stats)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_monitoring_classes(self):
        """
        Verify monitoring classes endpoint

        tests:
        - If Url is ok
        """

        response = self.client.get(self.url_classes)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_monitoring_table_filter_co_cr(self):
        """
        Verify CO_CR filter

        tests:
        - If Url is ok
        - If all results filtered matches params
        """

        kwargs = {'co_cr': str(self.co_cr)}
        response_filtered = self.client.get(
            self.url_table, kwargs)

        queryset_co_cr = self.queryset.filter(co_cr=self.co_cr)
        self.assertEqual(len(response_filtered.data),
                         queryset_co_cr.count())

        for i in response_filtered.json():
            self.assertEqual(int(i['co_cr']), int(self.co_cr))

    def test_monitoring_table_filter_co_funai(self):
        """
        Verify CO_FUNAI filter

        tests:
        - If Url is ok
        - If all results filtered matches params
        """

        kwargs = {'co_funai': str(self.co_funai)}
        response_filtered = self.client.get(
            self.url_table, kwargs)

        queryset_co_funai = self.queryset.filter(co_funai=self.co_funai)
        self.assertEqual(len(response_filtered.data),
                         queryset_co_funai.count())

        for i in response_filtered.json():
            self.assertEqual(int(i['co_funai']), int(self.co_funai))

    def test_monitoring_table_filter_stage(self):
        """
          Verify STAGE filter

          tests:
          - If Url is ok
          - If all results filtered matches params
          """

        kwargs = {'stage': str(self.no_estagio)}
        response_filtered = self.client.get(
            self.url_table, kwargs)

        queryset_stage = self.queryset.filter(no_estagio=self.no_estagio)
        self.assertEqual(len(response_filtered.data),
                         queryset_stage.count())

    def test_monitoring_table_filter_start_end_date(self):
        """
          Verify start end date filter

          tests:
          - If Url is ok
          - If all results filtered matches params
          """

        #     # Filtering results since 2015 (first date)

        #     # Filtering results between 2020 and 2021
        kwargs = {'start_date': '2020-12-01', 'end_date': '2021-12-31'}
        response_filtered = self.client.get(self.url_table, kwargs)
        queryset_dates = self.queryset.filter(
                dt_t_um__gte='2020-12-01', dt_t_um__lte='2021-12-31')

        self.assertEqual(len(response_filtered.data), queryset_dates.count())

    def test_view_request_url_with_wrong_filters(self):
        """
            Verify All filters with wrong params
        """

        kwargs = {"start_date": "2020-20-13"}
        response = self.client.get(self.url_table, kwargs)
        self.assertTrue(status.is_client_error(response.status_code))

        kwargs = {"end_date": "2018-MM-14"}
        response = self.client.get(self.url_table, kwargs)
        self.assertTrue(status.is_client_error(response.status_code))

        kwargs = {"end_date": 'None', "start_date": "2018-13-13"}
        response = self.client.get(self.url_table, kwargs)
        self.assertTrue(status.is_client_error(response.status_code))

        kwargs = {"end_date": '1', "start_date": 'None'}
        response = self.client.get(self.url_table, kwargs)
        self.assertTrue(status.is_client_error(response.status_code))

    def test_table_stats(self):
        """
         Verify monitoring table stats endpoint

         tests:
         - If Url is ok
        """
        response = self.client.get(self.url_table_stats)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @ classmethod
    def tearDownClass(cls):
        """TearDown for Class."""
        pass
