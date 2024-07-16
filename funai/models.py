from django.contrib.gis.db import models
from django.utils.translation import ugettext_lazy as _


class CoordenacaoRegional(models.Model):
    """Models for Regional Coordenation."""

    co_cr = models.BigIntegerField(
        _('Regional Coordenation code'),
        unique=True,
        primary_key=True,
        default=1
    )

    ds_cr = models.CharField(
        _('Regional Coordenation name'),
        max_length=255,
        blank=True,
        null=True
    )

    no_abreviado = models.CharField(
        _('Regional Coordenation acronym'),
        max_length=255,
        blank=True,
        null=True
    )

    sg_cr = models.CharField(
        _('Regional Coordenation flag'),
        max_length=255,
        blank=True,
        null=True
    )

    st_situacao = models.CharField(
        _('Situation'),
        max_length=255,
        blank=True,
        null=True
    )

    ds_email = models.CharField(
        _('Email'),
        max_length=255,
        blank=True,
        null=True
    )

    no_regiao = models.CharField(
        _('Region name'),
        max_length=255,
        blank=True,
        null=True
    )

    no_municipio = models.CharField(
        _('City name'),
        max_length=255,
        blank=True,
        null=True
    )

    no_uf = models.CharField(
        _('State'),
        max_length=255,
        blank=True,
        null=True
    )

    sg_uf = models.CharField(
        _('State acronym'),
        max_length=255,
        blank=True,
        null=True
    )

    ds_telefone = models.CharField(
        _('Contact number'),
        max_length=512,
        blank=True,
        null=True
    )

    dt_cadastro = models.DateTimeField(
        _('Register date'),
        blank=True,
        null=True
    )

    class Meta:
        """Metaclass to `funai.CoordenacaoRegional`."""
        app_label = 'funai'
        verbose_name = 'CoordenacaoRegional'
        verbose_name_plural = 'CoordenacoesRegionais'

    def __str__(self) -> str:
        """Returns string for class based name.

        Returns:
            str: string for model data
        """
        return f'{self.co_cr} - {self.ds_cr}'


class LimiteTerraIndigena(models.Model):
    """Indigenous Lands model data.

    * Association:
        * Has one: `funai.CoordenacaoRegional`
    """

    geom = models.MultiPolygonField(
        srid=4674,
        blank=True,
        null=True
        )

    no_ti = models.CharField(
        _('Name of Indigenous Lands'),
        max_length=255,
    )
    co_funai = models.IntegerField(
        _('Funai code'),
        unique=True,
    )
    no_grupo_etnico = models.CharField(_("Grupo Étnico"),
                                       max_length=255,
                                       blank=True,
                                       null=True
                                       )
    ds_fase_ti = models.CharField(_("Fase TI"), max_length=100,
                                  blank=True,
                                  null=True)
    ds_modalidade = models.CharField(_("Modalidade TI"), max_length=100,
                                     blank=True,
                                     null=True)
    ds_reestudo_ti = models.CharField(_("Reestudo TI"), max_length=80,
                                      blank=True,
                                      null=True)
    ds_cr = models.CharField(max_length=100,         blank=True,
                             null=True)
    co_cr = models.ForeignKey(
        CoordenacaoRegional,
        to_field='co_cr',
        related_name='terras_indigenas',
        on_delete=models.DO_NOTHING,
        db_column='co_cr',
        db_constraint=False
    )
    no_municipio = models.TextField(blank=True,
                                    null=True)
    sg_uf = models.CharField(max_length=20,
                             blank=True,
                             null=True)
    st_faixa_fronteira = models.CharField(max_length=3,         blank=True,
                                          null=True)
    dt_em_estudo = models.DateField(blank=True,
                                    null=True)
    ds_portaria_em_estudo = models.TextField(blank=True,
                                             null=True)
    dt_delimitada = models.DateField(blank=True,
                                     null=True)
    ds_despacho_delimitada = models.TextField(blank=True,
                                              null=True)
    dt_declarada = models.DateField(blank=True,
                                    null=True)
    ds_portaria_declarada = models.TextField(blank=True,
                                             null=True)
    dt_homologada = models.DateField(blank=True,
                                     null=True)
    ds_decreto_homologada = models.TextField(blank=True,
                                             null=True)
    dt_regularizada = models.DateField(blank=True,
                                       null=True)
    ds_matricula_regularizada = models.TextField(blank=True,
                                                 null=True)
    ds_doc_resumo_em_estudo = models.TextField(blank=True,
                                               null=True)
    ds_doc_resumo_delimitada = models.TextField(blank=True,
                                                null=True)
    ds_doc_resumo_declarada = models.TextField(blank=True,
                                               null=True)
    ds_doc_resumo_homologada = models.TextField(blank=True,
                                                null=True)
    ds_doc_resumo_regularizada = models.TextField(blank=True,
                                                  null=True)

    st_amazonia_legal = models.BooleanField(blank=True,
                                            null=True)
    nu_area_ha = models.DecimalField(max_digits=100, decimal_places=2,
                                     blank=True,
                                     null=True)
    dt_cadastro = models.DateTimeField(blank=True,
                                       null=True)

    possui_ig = models.BooleanField(
        default= False
    )   

    def __str__(self):
        return str(self.no_ti)
    
    class Meta:
        """Metaclass to `funai.LimiteTerraIndigena`."""
        app_label = 'funai'
        verbose_name = _('Indigenous Lands')
        verbose_name_plural = _('Indigenous Lands')
        ordering = ('no_ti', )

class InstrumentoGestaoFunai(models.Model):
    """Instrumental Indigenous Lands model data.

    * Association:
        * Has one: `funai.LimiteTerraIndigena`
    """

    co_funai = models.IntegerField(
        blank=False,
        null=False
    )
    no_ti = models.CharField(
        _('Name of Indigenous Lands'),
        max_length=255,
        blank=True,
        null=True
    )
    no_regiao = models.CharField(
        _('Region Name'),
        max_length=255,
        blank=True,
        null=True
    )
    sg_uf = models.CharField(
        _('State aconymn'),
        max_length=255,
        blank=True,
        null=True
    )
    no_povo = models.CharField(
        _('Hamlet Names'),
        max_length=255,
        blank=True,
        null=True
    )
    no_bioma = models.CharField(
        _('Biom Name'),
        max_length=255,
        blank=True,
        null=True
    )
    ds_parceiros = models.CharField(
        _('Partners'),
        max_length=255,
        blank=True,
        null=True
    )
    cr_funai = models.CharField(
        _('Name Funai'),
        max_length=255,
        blank=True,
        null=True
    )
    no_ig = models.CharField(
        _('Instrumental Name'),
        max_length=255,
        blank=True,
        null=True
    )
    ds_status = models.CharField(
        _('status'),
        max_length=255,
        blank=True,
        null=True
    )
    nu_ano_elaboracao = models.IntegerField(
        _('Elaborated in'),
        blank=True,
        null=True
    )
    ds_disp_meio_local = models.CharField(
        _('Privided by'),
        max_length=255,
        blank=True,
        null=True
    )
    ds_tll_publi = models.CharField(
        _(''),
        max_length=255,
        blank=True,
        null=True
    )
    ds_obs = models.CharField(
        _(''),
        max_length=255,
        blank=True,
        null=True
    )
    dt_cadastro = models.DateField(
        _('Register Date'),
        blank=True,
        null=True
    )


    class Meta:
        """Metaclass to `funai.tb_instrumento_gestao_funai`."""
        app_label = 'funai'
        db_table = 'tb_instrumento_gestao_funai'
        verbose_name = _('Management Instrument')
        verbose_name_plural = _('Management Instruments')