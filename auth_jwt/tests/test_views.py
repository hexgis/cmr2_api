from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from .recipes import Recipes


class TestTokenViews(APITestCase):
    """Test case for simple jwt token views.

    Args:
        APITestCase (class 'rest_framework.test.APITestCase'): Includes a few
            helper classes that extend Django's existing test framework.
    """

    def setUp(self):
        """Set up data for tests, created user and setting urls."""

        self.recipes = Recipes()
        self.recipes.user.make()

        self.client = APIClient()
        self.token_url = reverse('auth:token_obtain_pair')
        self.refresh_url = reverse('auth:token_refresh')

    def test_token_generate_correct_password(self):
        """Test token generate with user correct passwor."""

        data = {'username': 'user', 'password': 'top_secret'}
        request = self.client.post(self.token_url, data=data, format='json')

        self.assertTrue(status.is_success(request.status_code))
        self.assertTrue(request.data)
        self.assertTrue(request.data['access'])
        self.assertTrue(request.data['refresh'])

    def test_token_generate_incorrect_password(self):
        """Test token generate with user incorrect password."""

        data = {'username': 'user', 'password': 'incorrect'}
        request = self.client.post(self.token_url, data=data, format='json')
        self.assertTrue(status.is_client_error(request.status_code))

    def test_refresh_generate(self):
        """Test refresh token generate with access token."""

        data = {
            'username': 'user',
            'password': 'top_secret'
        }
        request = self.client.post(self.token_url, data=data, format='json')
        self.assertTrue(status.is_success(request.status_code))

        data = {'refresh': request.data['refresh']}
        request = self.client.post(self.refresh_url, data=data, format='json')

        self.assertTrue(status.is_success(request.status_code))
        self.assertTrue(request.data['access'])


class TestChangePasswordView(APITestCase):
    """Test case for auth module (change password) view.

    Args:
        APITestCase (class 'rest_framework.test.APITestCase'): Includes a few
            helper classes that extend Django's existing test framework.
    """

    def setUp(self):
        """Set up data for tests, created user and setting urls."""

        self.recipes = Recipes()
        self.recipes.user.make()

        self.client = APIClient()
        self.token_url = reverse('auth:token_obtain_pair')

        data = {'username': 'user', 'password': 'top_secret'}
        request = self.client.post(self.token_url, data=data, format='json')

        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + request.data['access'])
        self.change_url = reverse('auth:change-password')

    def test_change_password_without_data(self):
        """Test change password without request data."""
        with self.assertRaises(Exception):
            self.client.put(self.change_url, data={}, format='json')

    def test_change_password_incorrect_password(self):
        """Test change password with incorrect passwor."""

        data = {'oldPassword': 'incorrect', 'newPassword1': 'top_secret'}
        request = self.client.put(self.change_url, data, format='json')

        self.assertTrue(status.is_client_error(request.status_code))

    def test_change_password_correct(self):
        """Test change password with correct password and request data."""

        data = {'oldPassword': 'top_secret', 'newPassword1': 'new_top_secret'}
        request = self.client.put(self.change_url, data, format='json')

        self.assertTrue(status.is_success(request.status_code))
        self.assertTrue(request.data['access'])
        self.assertTrue(request.data['refresh'])
        self.assertTrue(User.objects.first().check_password('new_top_secret'))

    def test_change_password_without_user(self):
        """Test change password without authentication."""

        client = APIClient()
        data = {'oldPassword': 'top_secret', 'newPassword1': 'new_top_secret'}
        request = client.put(self.change_url, data, format='json')

        self.assertEquals(request.status_code, status.HTTP_401_UNAUTHORIZED)
