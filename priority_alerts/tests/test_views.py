from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from rest_framework import status

from django.urls import reverse

from django.contrib.auth.models import User


class UrgentAlertsViewsTests(APITestCase):
    """Test case PiorirityConsolidatedViewTests data.

    Args:
        APITestCase (class 'rest_framework.test.APITestCase'): Includes a few
            helper classes that extend Django's existing test framework.
    """

    def get_requered_filters_parameters(self):
        """Creating parameters requered applied to filters."""

        parameter = {
            'co_funai':20702,
            'co_cr': 30202001962,
            'start_date': '2021-07-28',
            'end_date': '2021-12-15',
            'pk_detail': 13
        }

        return parameter

    @classmethod
    def setUpTestData(cls):
        """Settings URLs APP priority_alerts for tests."""

        cls.parameters = cls.get_requered_filters_parameters(cls)

        cls.url_alerts = reverse(
            'alerts:alerts'
        )
        cls.url_alerts_table = reverse(
            'alerts:alerts-table'
        )
        cls.url_alerts_detail = reverse(
            'alerts:alerts-detail',
            kwargs={'id': cls.parameters['pk_detail']}
        )
        cls.url_alerts_map_stats = reverse(
            'alerts:alerts-map-stats'
        )
        cls.url_alerts_classes = reverse(
            'alerts:alerts-classes'
        )

    def setUp(self):
        """Set up data for tests, created user."""

        self.user = User.objects.create_superuser(
            username='user_test', password='top_secret'
        )
        self.user = User.objects.create_user(
            username="jacob", email="jacob@…", password="top_secret"
        )
        self.client = APIClient()

    def test_url_pioririty_consolidated(self):
        """Test url pioririty consolidated."""

        res = self.client.get(self.url_alerts, {
            'start_date': self.parameters['start_date'],
            'end_date': self.parameters['end_date']})

        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_url_alerts_table(self):
        """Test url pioririty consolidated table."""

        res = self.client.get(self.url_alerts_table, {
            'start_date': self.parameters['start_date'],
            'end_date': self.parameters['end_date']})

        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_url_alerts_detail(self):
        """Test url pioririty consolidated detail."""

        res = self.client.get(self.url_alerts_detail)

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_url_alerts_stats(self):
        """Test url pioririty consolidated map stats."""

        res = self.client.get(self.url_alerts_map_stats, {
            'start_date': self.parameters['start_date'],
            'end_date': self.parameters['end_date']})

        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_url_alerts_priorities(self):
        """Test url pioririty consolidated priorities."""

        res = self.client.get(self.url_alerts_classes)

        self.assertEqual(res.status_code, status.HTTP_200_OK)


class UrgentAlertsFiltersViewsTests(APITestCase):
    """Test case PiorirityConsolidatedFiltersViewsTests data."""

    #TODO: End filter tests on class UrgentAlertsFiltersViewsTests
    pass
