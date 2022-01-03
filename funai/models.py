from django.db import models
from django.db.models.deletion import DO_NOTHING, SET_NULL
from django.db.models.fields import related
from django.utils.translation import ugettext_lazy as _


class CoordenacaoRegional(models.Model):
  # co_cr = models.BigIntegerField(
  #   unique=True,
  #   blank=True,
  #   null=True
  # )
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
  nu_area_ha = models.IntegerField(
    blank=True,
    null=True
  )
  st_faixa_fronteira = models.CharField(
    max_length=255,
    blank=True,
    null=True
  )
  co_cr_fk = models.ForeignKey(
    'funai.CoordenacaoRegional',
    #'funai.CoordenacaoRegional.co_cr',
    on_delete=DO_NOTHING,
    #on_delite=SET_NULL, #Verificar qual dos dois ficará
    related_name='CO_CR_with_CO_TI'
  )
  class Meta:
      app_label = 'funai'
      verbose_name = 'LimiteTerraIndigena'
      verbose_name_plural = 'LimitesTerrasIndigenas'
      ordering = ["no_ti"]

#     # id_cont= models.IntegerField(
# 	# 	blank=True,
# 	# 	null=True,
#     # )
#     no_ti = models.CharField(
#         max_length=255,
#         blank=True,
#         null=True,
#     )
#     no_grupo_etnico= models.CharField(
#         max_length=255,
# 		blank=True,
# 		null=True,
#     )
#     ds_fase_ti= models.CharField(
#         max_length=255,
# 		blank=True,
# 		null=True,
#     )
#     ds_modalidade= models.CharField(
#         max_length=255,
# 		blank=True,
# 		null=True,
#     )
#     ds_reestudo_ti= models.CharField(
#         max_length=255,
# 		blank=True,
# 		null=True,
#     )
#     ds_cr= models.CharField(
#         max_length=255,
# 		blank=True,
# 		null=True,
#     )
#     no_municipio= models.CharField(
#         max_length=255,
# 		blank=True,
# 		null=True,
#     )
#     sg_uf= models.CharField(
#         max_length=255,
# 		blank=True,
# 		null=True,
#     )
#     co_funai= models.IntegerField(
# 		blank=True,
# 		null=True,
#     )
#     nu_area_ha= models.DecimalField(
#         max_digits=19,
#         decimal_places=10,
#         blank=True,
# 		null=True,
#     )
#     dt_cadastro= models.CharField(
#         max_length=255,
# 		blank=True,
# 		null=True,
#     )
#     st_faixa_fronteira= models.CharField(
#         max_length=255,
# 		blank=True,
# 		null=True,
#     )
#     dt_em_estudo= models.CharField(
#         max_length=255,
# 		blank=True,
# 		null=True,
#     )
#     ds_portaria_em_estudo= models.CharField(
#         max_length=512,
# 		blank=True,
# 		null=True,
#     )
#     dt_delimitada= models.CharField(
#         max_length=255,
# 		blank=True,
# 		null=True,
#     )
#     ds_despacho_delimitada= models.CharField(
#         max_length=255,
# 		blank=True,
# 		null=True,
#     )
#     dt_declarada= models.CharField(
#         max_length=255,
# 		blank=True,
# 		null=True,
#     )
#     ds_portaria_declarada= models.CharField(
#         max_length=255,
# 		blank=True,
# 		null=True,
#     )
#     dt_homologada= models.CharField(
#         max_length=255,
# 		blank=True,
# 		null=True,
#     )
#     ds_decreto_homologada= models.CharField(
#         max_length=255,
# 		blank=True,
# 		null=True,
#     )
#     dt_regularizada= models.CharField(
#         max_length=255,
# 		blank=True,
# 		null=True,
#     )
#     ds_matricula_regularizada= models.CharField(
#         max_length=255,
#  		blank=True,
# 		null=True,
#     )
#     ds_doc_resumo_em_estudo= models.CharField(
#         max_length=255,
# 		blank=True,
# 		null=True,
#     )
#     ds_doc_resumo_delimitada= models.CharField(
#         max_length=512,
# 		blank=True,
# 		null=True,
#     )
#     ds_doc_resumo_declarada= models.CharField(
#         max_length=512,
# 		blank=True,
# 		null=True,
#     )
#     ds_doc_resumo_homologada= models.CharField(
#         max_length=255,
#  	    blank=True,
# 		null=True,
#     )
#     ds_doc_resumo_regularizada= models.CharField(
#         max_length=255,
# 		blank=True,
# 		null=True,
#     )
#     co_cr= models.IntegerField(
# 		blank=True,
# 		null=True,
#     )
#     geom = models.GeometryField(
#         _('Geometry Field'),
#         srid=4326,
#         blank=True,
#         null=True,
#     )

