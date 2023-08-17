from rest_framework.test import APITestCase

from django.core.management import call_command

from priority_monitoring import models


class PriorityConsolidatedTest(APITestCase):
    """ Test case `models.PriorityConsolidated` model.

    Args:
        APITestCase (class 'rest_framework.test.APITestCase'): Includes a few
            helper classes that extend Django's existing test framework.
    """

    @classmethod
    def setUpTestData(cls):
        """Class variables using data load from fixtures file."""

        call_command(
            'loaddata',
            'priority_monitoring/fixtures/priority_consolidated.yaml',
            verbosity=0
        )

    def test_objects_created(self):
        """Test if object PriorityConsolidated is created."""

        self.assertTrue(models.PriorityConsolidated.objects.exists())

    def test_object_model_output_is_dt_t_zero_dt_t_um(self):
        """Verify the returns string in PriorityConsolidated class base name."""

        priority_output = models.PriorityConsolidated.objects.first()
        expected_object_name = '%s - %s' % (priority_output.dt_t_zero, priority_output.dt_t_um)

        self.assertEqual(str(priority_output), expected_object_name)
