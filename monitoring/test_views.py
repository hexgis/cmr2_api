from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient


class MonitoringFiltersTestCase(APITestCase):
    """ Test case MonitoringFiltersTestCase data."""

    @classmethod
    def setUpClass(cls):
        """SetUp for Class."""
        cls.client = APIClient()
        cls.monitoring_url = 'http://localhost:8080/monitoring/consolidated/'

    def setUp(self):
        """SetUp for methods."""
        pass

    def tearDown(self):
        """TearDown for methods."""
        pass

    def test_if_filters_is_correct(self):
        # Make request
        response = self.client.get(self.monitoring_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @classmethod
    def tearDownClass(cls):
        """TearDown for Class."""
        pass
