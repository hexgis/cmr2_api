from django.db import models

# Create your models here.


class UrgentAlerts(models.Model):
    "id"
    "no_ciclo"
    "no_titulo"
    "no_arquivo"
    "nu_referencia"
    "nu_mapa"
    "no_estagio"
    "no_estadio_nu_area_ha"
    "no_imagem"
    "nu_orbita_ponto"
    "dt_t_zero"
    "dt_t_um"
    "nu_area_ha"
    "nu_longitude_latitude"
    "co_funai"
    "no_ti"
    "ds_cr"
    "no_municipio"
    "dt_t_um_dte"
    "geom_as_wkt"
    class Meta:
        app_label = 'priority_alerts'
        verbose_name = 'Priority Alert'
        verbose_name_plural = 'Priorities Alerts'
        # db_table = 'funai\".\"vw_alerta_urgente_consolidado_a'
        # managed = False
