from django.db import models
from django.utils.translation import ugettext_lazy as _


class CoordenacaoRegional(models.Model):
  co_cr = models.BigIntegerField(
    # _('CR code'),
    unique=True,
    primary_key=True,
    default=9999
  )
  no_cr = models.CharField(
    max_length=255,
    blank=True,
    null=True
  )
  no_abreviado = models.CharField(
    max_length=255,
    blank=True,
    null=True
  )
  sg_cr = models.CharField(
    max_length=255,
    blank=True,
    null=True
  )
  st_situacao = models.CharField(
    max_length=255,
    blank=True,
    null=True
  )
  ds_email = models.CharField(
    max_length=255,
    blank=True,
    null=True
  )
  no_regiao = models.CharField(
    max_length=255,
    blank=True,
    null=True
  )
  no_municipio = models.CharField(
    max_length=255,
    blank=True,
    null=True
  )
  no_uf = models.CharField(
    max_length=255,
    blank=True,
    null=True
  )
  sg_uf = models.CharField(
    max_length=255,
    blank=True,
    null=True
  )
  ds_telefone = models.CharField(
    max_length=512,
    blank=True,
    null=True
  )
  dt_cadastro = models.DateTimeField(
    blank=True,
    null=True
  )
  class Meta:
    app_label = 'funai'
    verbose_name = 'CoordenacaoRegional'
    verbose_name_plural = 'CoordenacoesRegionais'
    ordering = ["no_cr"]

class LimiteTerraIndigena(models.Model):
  co_funai = models.IntegerField(
    unique=True,
    blank=True,
    null=True
  )
  no_ti = models.CharField(
    max_length=255,
    blank=True,
    null=True,
  )
  no_ti = models.CharField(
    max_length=255,
    blank=True,
    null=True
  )
  ds_fase_ti = models.CharField(
    max_length=255,
    blank=True,
    null=True
  )
  ds_modalidade = models.CharField(
    max_length=255,
    blank=True,
    null=True
  )
  ds_cr = models.CharField(
    max_length=255,
    blank=True,
    null=True
  )
  sg_uf = models.CharField(
    max_length=255,
    blank=True,
    null=True
  )
  co_funai = models.IntegerField(
    blank=True,
    null=True
  )
  nu_area_ha = models.DecimalField(
    max_digits=19,
    decimal_places=10,
    blank=True,
    null=True
  )
  nu_area_km = models.DecimalField(
    max_digits=19,
    decimal_places=10,
    blank=True,
    null=True
  )
  st_faixa_fronteira = models.CharField(
    max_length=255,
    blank=True,
    null=True
  )
  co_cr = models.ForeignKey(
    'funai.CoordenacaoRegional',
    on_delete=models.DO_NOTHING,
    related_name='CO_CR',
    null=True
  )
#   geom = models.GeometryField(
#       _('Geometry Field'),
#       srid=4326,
#       blank=True,
#       null=True,
#   )
  class Meta:
      app_label = 'funai'
      verbose_name = 'LimiteTerraIndigena'
      verbose_name_plural = 'LimitesTerrasIndigenas'
      ordering = ["no_ti"]