from django.test import TestCase
from monitoring import models


class MonitoringModelTest(TestCase):

    def test_monitoring_consolidated(self):
        model = models.MonitoringConsolidated
        model.objects.create(
            id=1,
            no_imagem='TEST_LC08_L1TP_225069_20200914_20200914_01_RT_r6g5b4',
            dt_imagem='2020-10-18',
            no_estagio='FF',
            nu_orbita=253,
            no_ciclo=38,
            nu_ponto=123,
            nu_latitude=99,
            nu_longitude=99,
            dt_t_zero='2019-08-24',
            dt_t_um='2019-08-24',
            dt_cadastro='2019-08-24',
            co_funai=7301,
            nu_area_km2=2.007029,
            nu_area_ha=200.702914,
            co_cr=30202001845,
            ds_cr='COORDENACAO REGIONAL ALTO PURUS',
            no_ti='Cabeceira do Rio Acre',
            ti_nu_area_ha='79089.306594',
            geom="MultiPolygon  (((-49.94545556 -4.4815375, -49.94521677 -4.4815375, -49.94521677 -4.48193481, -49.94519194 -4.48203414, -49.94566375 -4.48203414, -49.94572372 -4.48175426, -49.94548198 -4.48173124, -49.94545556 -4.4815375)))"
        )
        queryset = models.MonitoringConsolidated.objects.all()
        self.assertEqual(queryset.count(), 1)
