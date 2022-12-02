from email.mime import image
from django.test import TestCase

from catalog import models

# from django.test import TestCase
# from whatever.models import Whatever
from django.utils import timezone
# from django.core.urlresolvers import reverse


# models test
class CatalogsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        models.Catalogs.objects.create(
            objectid= 175
            image= "LC08_L1TP_225064_20180824_20180824_01_RT_r6g5b4.TIF"
            image_path= "media/LC08/225/064/LC08_L1TP_225064_20180824_20180824_01_RT/LC08_L1TP_225064_20180824_20180824_01_RT_r6g5b4.TIF"
            url_tms= "http://cmr.funai.gov.br/tms/LC08_L1TP_225064_20180824_20180824_01_RT_r6g5b4.xml"
            date= 2018-08-24
            pr_date= 2018-08-28
            cloud_cover= 5.88
            locator= "225/06"
            preview= ""
            sat= 2
            max_native_zoom= 15
            type= ""
            geom= "POLYGON ((-51.24392878899993 -6.591365817999933, -51.25714155399993 -6.653614304999933, -51.2599 -6.66661, -51.25990600999993 -6.6666091269999335, -52.9153 -6.42615, -52.90227601399993 -6.365621291999935, -52.60418556899994 -4.980252095999933, -52.588 -4.90503, -50.936951530999934 -5.144872513999934, -50.9369 -5.14488, -51.24392878899993 -6.591365817999933))"

        )
        
    def test_object_name_is_image(self):
        catalog_image = models.Catalogs.objects.get(id=1)
        expected_object_name = f'{catalog_image.image}'
        self.assertEqual(expected_object_name = str(image))
        
        
    # def create_whatever(self, title="only a test", body="yes, this is only a test"):
    #     return Whatever.objects.create(title=title, body=body, created_at=timezone.now())

    # def test_whatever_creation(self):
    #     w = self.create_whatever()
    #     self.assertTrue(isinstance(w, Whatever))
    #     self.assertEqual(w.__unicode__(), w.title)
        
class SatelliteTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        models.Satellite.objects.create(identifier="Spot", name="SatelliteSpot", describe="Satelite orbital com resolução X")

    def test_object_model_exit_is_name_or_identifier(self):
        satellite = models.Satellite.objects.get(id=1)
        expected_object = f'{satellite.name} or {satellite.identifier}'
        self.assertEqual(expected_object = str(name) or str(identifier))

    
    str(self.name) or str(self.identifier)
    