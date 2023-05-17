from rest_framework.test import APITestCase, APIClient
from rest_framework import status

from django.core.management import call_command
from django.urls import reverse

from funai import models


class FuaniViewsTests(APITestCase):
    """Test case FuaniViewsTests data."""
    @classmethod
    def setUpTestData(cls):
        """Class variables APP URLs."""
        cls.url_funai_cr = reverse('funai:coordenacao-regional')
        cls.url_funai_ti = reverse('funai:terras-indigenas')
        cls.parameter_co_cr_nonexistent = 99999999

    def setUp(self):
        """SetUp for methods."""
        self.client = APIClient()
        #TODO: After adding authentication and authorization in the FUNAI APP.
        # from django.test import RequestFactory
        # from django.contrib.auth.models import User
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
    
    def test_url__terra_indigena_invalid_co_cr(self):
        request = self.client.get(
            self.url_funai_ti, {'co_cr':self.parameter_co_cr_nonexistent,})
        
        self.assertEqual(
            request.status_code, status.HTTP_400_BAD_REQUEST,
            'id_acao valid is requirid. Expected Response Code 400, received \
                {0}:{1} instead.' .format(
                    request.status_code,request.status_text))

class FuaniViewsFiltersTests(APITestCase):
    """Test case FuaniViewsFiltersTests data."""
    @classmethod
    def setUpTestData(cls):
        """Class variables using in load data fixtures file end URLs."""
        cls.url_funai_ti = reverse('funai:terras-indigenas')
        cls.parameter = 30202001962

        call_command('loaddata', 'funai/fixtures/coordenacao_regional.yaml',
            verbosity=0)
        call_command('loaddata', 'funai/fixtures/terras_indigenas.yaml',
            verbosity=0)

    def setUp(self):
        """SetUp for methods."""
        self.client = APIClient()
        # self.client.force_authenticate(user=self.user)

        self.queryset_valid = models.LimiteTerraIndigena.objects.filter(
            co_cr_id=self.parameter)
        self.request_valid = self.client.get(self.url_funai_ti, {
            'co_cr':self.parameter,})

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
