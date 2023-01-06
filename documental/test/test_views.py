from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.core.management import call_command


class DocumentalTestCase(TestCase):
    """ Test case DocumentalTestCase data."""

    @classmethod
    def setUpTestData(cls):
        """
            SetUp for Class.
            Call test data
        """

        call_command(
            'loaddata', 'documental/fixtures/documental_docs_action.yaml', verbosity=0)
        call_command(
            'loaddata', 'documental/fixtures/documental_users_who_registered.yaml', verbosity=0)
        call_command(
            'loaddata', 'documental/fixtures/documental_docs.yaml', verbosity=0)

        cls.list_actions = reverse('documental:list-actions')
        cls.list_doc = reverse('documental:list-doc')
        cls.upload = reverse('documental:upload-doc')

    def setUp(self):
        """SetUp for methods."""
        self.client = APIClient()

    def test_list_actions_document_root(self):
        """
            Verify source endpoint

            tests:
            - If Url is ok
        """
        kwargs = {'action_type': 'DOCUMENT_ROOT'}
        response = self.client.get(self.list_actions, kwargs)
        self.assertTrue(status.is_success(response.status_code))

    def test_list_actions_documents_ti(self):
        """
            Verify source endpoint

            tests:
            - If Url is ok
        """
        kwargs = {'action_type': 'DOCUMENTS_TI'}
        response = self.client.get(self.list_actions, kwargs)
        self.assertTrue(status.is_success(response.status_code))

    def test_list_actions_mapoteca(self):
        """
            Verify source endpoint

            tests:
            - If Url is ok
        """
        kwargs = {'action_type': 'MAPOTECA'}
        response = self.client.get(self.list_actions, kwargs)
        self.assertTrue(status.is_success(response.status_code))

    def test_list_doc(self):
        """
            Verify source endpoint

            tests:
            - If Url is ok
        """
        kwargs = {'id_acao': 12}
        response = self.client.get(self.list_doc, kwargs)
        self.assertTrue(status.is_success(response.status_code))

    # def test_upload(self):
    #     response = self.client.get(self.upload)
    #     self.assertTrue(status.is_success(response.status_code))
