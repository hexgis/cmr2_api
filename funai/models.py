from django.db import models
from django.utils.translation import ugettext_lazy as _


class LimiteTerraIndigena(models.Model):
    # id_cont= models.IntegerField(
	# 	blank=True,
	# 	null=True,
    # )
    no_ti = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )
    no_grupo_etnico= models.CharField(
        max_length=255,
		blank=True,
		null=True,
    )
    ds_fase_ti= models.CharField(
        max_length=255,
		blank=True,
		null=True,
    )
    ds_modalidade= models.CharField(
        max_length=255,
		blank=True,
		null=True,
    )
    ds_reestudo_ti= models.CharField(
        max_length=255,
		blank=True,
		null=True,
    )
    ds_cr= models.CharField(
        max_length=255,
		blank=True,
		null=True,
    )
    no_municipio= models.CharField(
        max_length=255,
		blank=True,
		null=True,
    )
    sg_uf= models.CharField(
        max_length=255,
		blank=True,
		null=True,
    )
    co_funai= models.IntegerField(
		blank=True,
		null=True,
    )
    nu_area_ha= models.DecimalField(
        max_digits=19,
        decimal_places=10,
        blank=True,
		null=True,
    )
    dt_cadastro= models.CharField(
        max_length=255,
		blank=True,
		null=True,
    )
    st_faixa_fronteira= models.CharField(
        max_length=255,
		blank=True,
		null=True,
    )
    dt_em_estudo= models.CharField(
        max_length=255,
		blank=True,
		null=True,
    )
    ds_portaria_em_estudo= models.CharField(
        max_length=512,
		blank=True,
		null=True,
    )
    dt_delimitada= models.CharField(
        max_length=255,
		blank=True,
		null=True,
    )
    ds_despacho_delimitada= models.CharField(
        max_length=255,
		blank=True,
		null=True,
    )
    dt_declarada= models.CharField(
        max_length=255,
		blank=True,
		null=True,
    )
    ds_portaria_declarada= models.CharField(
        max_length=255,
		blank=True,
		null=True,
    )
    dt_homologada= models.CharField(
        max_length=255,
		blank=True,
		null=True,
    )
    ds_decreto_homologada= models.CharField(
        max_length=255,
		blank=True,
		null=True,
    )
    dt_regularizada= models.CharField(
        max_length=255,
		blank=True,
		null=True,
    )
    ds_matricula_regularizada= models.CharField(
        max_length=255,
 		blank=True,
		null=True,
    )
    ds_doc_resumo_em_estudo= models.CharField(
        max_length=255,
		blank=True,
		null=True,
    )
    ds_doc_resumo_delimitada= models.CharField(
        max_length=512,
		blank=True,
		null=True,
    )
    ds_doc_resumo_declarada= models.CharField(
        max_length=512,
		blank=True,
		null=True,
    )
    ds_doc_resumo_homologada= models.CharField(
        max_length=255,
 	    blank=True,
		null=True,
    )
    ds_doc_resumo_regularizada= models.CharField(
        max_length=255,
		blank=True,
		null=True,
    )
    co_cr= models.IntegerField(
		blank=True,
		null=True,
    )
    geom = models.GeometryField(
        _('Geometry Field'),
        srid=4326,
        blank=True,
        null=True,
    )

class CoordenacaoRegional(models.Model):
    co_cr= models.IntegerField(
		blank=True,
		null=True,
    )
    no_cr = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )
