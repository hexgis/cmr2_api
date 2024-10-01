from rest_framework.test import APITestCase

from django.core.management import call_command

from funai import models


class TestCoordenacaoRegionalModel(APITestCase):
    """ Test case `models.CoordenacaoRegional` model."""
    @classmethod
    def setUpTestData(cls):
        """Class variables using data load from fixtures file."""
        call_command('loaddata', 'funai/fixtures/coordenacao_regional.yaml',
            verbosity=0)
    
    def test_objects_created(self):
        """Test if object CoordenacaoRegional is created."""
        self.assertTrue(models.CoordenacaoRegional.objects.exists())

    def test_object_model_output_is_dt_t_zero_dt_t_um(self):
        """Verify the returns string in LimiteTerraIndigena class base name."""
        cr_model_output = models.CoordenacaoRegional.objects.first()
        expected_object_name = '%s - %s' % (
            cr_model_output.co_cr, cr_model_output.ds_cr)

        self.assertEqual(str(cr_model_output), expected_object_name)


class TestTerraIndigenaModelData(APITestCase):
    """ Test case `models.LimiteTerraIndigena` model."""
    @classmethod
    def setUpTestData(cls):
        """Class variables using data load from fixtures file."""
        call_command('loaddata', 'funai/fixtures/coordenacao_regional.yaml',
            verbosity=0)
        
        call_command('loaddata', 'funai/fixtures/terras_indigenas.yaml',
            verbosity=0)
    
    def test_objects_created(self):
        """Test if object LimiteTerraIndigena is created."""
        self.assertTrue(models.LimiteTerraIndigena.objects.exists())

class TestInstrumentoGestaoFunai(APITestCase):
    """ Teste case `models.InstrumentoGestaoFunai` model. """
    @classmethod
    def setUpTestData(cls):
        """ Class variables using data load from fixtures file. """
        call_command('loaddata', 'funai/fixtures/terras_indigenas.yaml',
            verbosity=0)
        
        call_command('loaddata', 'funai/fixtures/instrumento_gestao_funai.yaml',
            verbosity=0)

    def test_objects_created(self):
        """ Test if object InstrumentoGestaoFunai is created. """
        self.assertTrue(models.InstrumentoGestaoFunai.objects.exists())