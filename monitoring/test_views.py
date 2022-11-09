from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient


class MonitoringFiltersTestCase(APITestCase):
    """ Test case MonitoringFiltersTestCase data."""

    @classmethod
    def setUpClass(cls):
        """SetUp for Class."""
        cls.client = APIClient()
        cls.url_base = reverse('monitoring:monitoring')
        cls.url_detail = reverse('monitoring-detail')
        cls.url_map_stats = reverse('monitoring:monitoring-map-stats')
        cls.url_classes = reverse('monitoring:monitoring-classes')
        cls.url_table = reverse('monitoring:monitoring-table')
        cls.url_table_stats = reverse('monitoring:monitoring-table-stats')

    def setUp(self):
        """SetUp for methods."""

    def tearDown(self):
        """TearDown for methods."""
        pass

    # def test_if_filters_is_correct(self):
    #     home_url = reverse('monitoring:monitoring')
    #     self.assertEqual(home_url, '/')

    def url_source(self):
        # Make request
        response = self.client.get(self.url_base)
        self.assertEqual(self.url_map_stats, '/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_map_stats(self):
        # Make request
        response = self.client.get(self.url_map_stats)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_classes(self):
        # Make request
        response = self.client.get(self.url_classes)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_table(self):
        # Make request
        response = self.client.get(self.url_table)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_table_stats(self):
        # Make request
        response = self.client.get(self.url_table_stats)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @classmethod
    def tearDownClass(cls):
        """TearDown for Class."""
        pass
