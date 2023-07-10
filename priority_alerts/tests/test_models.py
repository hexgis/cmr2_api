from rest_framework.test import APITestCase

from django.core.management import call_command

from priority_alerts import models


class UrgentAlertsTests(APITestCase):
    """ Test case `models.UrgentAler` model.

    Args:
        APITestCase (class 'rest_framework.test.APITestCase'): Includes a few
            helper classes that extend Django's existing test framework.
    """

    @classmethod
    def setUpTestData(cls):
        """Class variables using data load from fixtures file."""
        print('APP Priority_alerts models-------------->>>>>>>>>>>>>>>>>>>  1')
        call_command(
            'loaddata',
            'priority_alerts/fixtures/urgent_alerts.yaml',
            verbosity=0)

    def test_objects_created(self):
        """Test if object UrgentAler is created."""

        self.assertTrue(models.UrgentAlerts.objects.exists())








































# how to test table managed false django
# https://medium.com/an-idea/testing-with-the-legacy-database-in-django-3be84786daba
# https://www.caktusgroup.com/blog/2010/09/24/simplifying-the-testing-of-unmanaged-database-models-in-django/
# https://www.caktusgroup.com/blog/2010/09/24/simplifying-the-testing-of-unmanaged-database-models-in-django/
# https://docs.djangoproject.com/en/dev/ref/models/options/#managed
# https://docs.djangoproject.com/en/dev/ref/models/options/#managed
# class YourTestClass(APITestCase):
#     @classmethod
#     def setUpTestData(cls):
#         print("setUpTestData: Run once to set up non-modified data for all class methods.")
#         pass

#     def setUp(self):
#         print("setUp: Run once for every test method to setup clean data.")
#         pass

#     def test_false_is_false(self):
#         print("Method: test_false_is_false.")
#        test_runnerone_equals_two(self):
#         print("Method: test_one_plus_one_equals_two.")
#         self.assertEqual(1 + 1, 2)


# from rest_framework.test import APITestCase
# class ExemploDeTest(APITestCase):
    
#     def test_false_is_false(self):
#         print("Method: test_false_is_false.")
#         print('xpto 1 -----------       priority_alerts')
#         self.assertFalse(False)

#     def test_false_is_true(self):
#         print("Method: test_false_is_true.")
#         print('xpto 2 -----------       priority_alerts')
#         self.assertTrue(True)

#     def test_one_plus_one_equals_two(self):
#         print("Method: test_one_plus_one_equals_two.")
#         print('xpto 3 -----------       priority_alerts')
#         self.assertEqual(1 + 1, 2)