from rest_framework.test import APITestCase

from django.core.management import call_command

from deter_monitoring import models


class DeterTITests(APITestCase):
    """Test case `models.deter_monitoring.LandUseTI` model.

    Args:
        APITestCase (class 'rest_framework.test.APITestCase'): Includes a few
            helper classes that extend Django's existing test framework.
    """

    @classmethod
    def setUpTestData(cls):
        """Class variables using dumpdata fixtures file."""

        call_command(
            'loaddata',
            'deter_monitoring/fixtures/deter_ti.yaml',
            verbosity=0)

    def test_objects_deterti_created(self):
        """Test if object DeterTI is created."""

        self.assertTrue(models.DeterTI.objects.exists())

    def test_object_output_name_is_image(self):
        """Test the model output is named Catalog Image"""
        deter_ti_model_output = models.DeterTI.objects.first()
        expected_object_name = '%s - %s - %s' % (deter_ti_model_output.path_row, deter_ti_model_output.view_date, deter_ti_model_output.classname)

        self.assertEqual(expected_object_name, str(deter_ti_model_output))


#TODO: Create test_views tests.
