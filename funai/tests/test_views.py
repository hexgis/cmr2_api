from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from django.core.management import call_command
from django.contrib.auth.models import User
from django.test import RequestFactory
from django.urls import reverse

from funai import models


class FuaniViewsTests(APITestCase):
    """Test case FuaniViewsTests data."""
    @classmethod
    def setUpTestData(cls):
        """Class variables APP URLs."""
        cls.url_funai_cr = reverse('funai:coordenacao-regional')
        cls.url_funai_ti = reverse('funai:terras-indigenas')

    def setUp(self):
        """SetUp for methods."""
        self.client = APIClient()
        # self.client.force_authenticate(user=self.user)

    def test_url_coordenacao_regional(self):
        """Test URL FUNAI CoordenacaoRegional."""
        request = self.client.get(self.url_funai_cr)

        self.assertEqual(
            request.status_code, status.HTTP_200_OK, 
            'Expected Response Code 200, received {0}:{1} instead.' .format(
                request.status_code,request.status_text))

    def test_url_terra_indigena(self):
        """Test URL FUNAI TerrasIndigenas."""
        request = self.client.get(self.url_funai_ti)

        self.assertEqual(
            request.status_code, status.HTTP_200_OK, 
            'Expected Response Code 200, received {0}:{1} instead.' .format(
                request.status_code,request.status_text))


class TestCoordenacaoRegionalViewsTests(APITestCase):
    """Test case TestCoordenacaoRegionalViewsTests data."""
    def get_requered_filters_parameters(self):
        """Creating parameters requered applied to filters."""
        parameter = {
            'co_cr': 30202001962,
        }

        return parameter

    @classmethod
    def setUpTestData(cls):
        """Class variables using in load data fixtures file end URLs."""
        cls.parameters = cls.get_requered_filters_parameters(cls)
        cls.url_funai_ti = reverse('funai:terras-indigenas')

        call_command('loaddata', 'funai/fixtures/coordenacao_regional.yaml',
            verbosity=0)
        call_command('loaddata', 'funai/fixtures/terras_indigenas.yaml', 
            verbosity=0)

    def setUp(self):
        """SetUp for methods."""
        self.client = APIClient()
        # self.client.force_authenticate(user=self.user)

        self.queryset_valid = models.LimiteTerraIndigena.objects.filter(
            co_cr_id=self.parameters['co_cr'])
        self.request_valid = self.client.get(self.url_funai_ti, {
            'co_cr':self.parameters['co_cr'],})

    def test_valid_parameters(self):
        """Test valid URL parameters in request."""
        request = self.request_valid

        self.assertEqual(request.status_code, status.HTTP_200_OK)

    def test_objects_queryset_created(self):
        """Test if object queryset is created."""
        qs = self.queryset_valid

        self.assertTrue(qs.exists())

    def test_request_filter_is_equals_len_queryset_filter(self):
        """test record amount of request is iqual to queyrsaf."""
        request = self.request_valid.json()
        qs = self.queryset_valid

        self.assertEqual(len(request), qs.count())
