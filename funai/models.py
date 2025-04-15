from django.contrib.gis.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone


class CoordenacaoRegional(models.Model):
    """Models for Regional Coordenation."""

    co_cr = models.BigIntegerField(
        _('COD Coordenção Regional'),
        unique=True,
        primary_key=True,
        default=1
    )

    ds_cr = models.CharField(
        _('Coordenação Regional'),
        max_length=255,
        blank=True,
        null=True
    )

    no_abreviado = models.CharField(
        _('UF Coordenação Regional'),
        max_length=255,
        blank=True,
        null=True
    )

    sg_cr = models.CharField(
        _('Sigla Coordenação Regional'),
        max_length=255,
        blank=True,
        null=True
    )

    st_situacao = models.CharField(
        _('Situação'),
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
        _('Região'),
        max_length=255,
        blank=True,
        null=True
    )

    no_municipio = models.CharField(
        _('Cidade'),
        max_length=255,
        blank=True,
        null=True
    )

    no_uf = models.CharField(
        _('Estado'),
        max_length=255,
        blank=True,
        null=True
    )

    sg_uf = models.CharField(
        _('UF'),
        max_length=255,
        blank=True,
        null=True
    )

    ds_telefone = models.CharField(
        _('TEL de Contato'),
        max_length=512,
        blank=True,
        null=True
    )

    dt_cadastro = models.DateTimeField(
        _('Data Registro'),
        blank=True,
        null=True
    )

    class Meta:
        """Metaclass to `funai.CoordenacaoRegional`."""
        app_label = 'funai'
        verbose_name = 'Coordenacao Regional'
        verbose_name_plural = 'Coordenacoes Regionais'
        managed = False

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
        _('Terra Indígema'),
        max_length=255,
    )

    co_funai = models.IntegerField(
        _('COD Funai'),
        unique=True,
    )

    no_grupo_etnico = models.CharField(
        _("Grupo Étnico"),
        max_length=255,
        blank=True,
        null=True
    )

    ds_fase_ti = models.CharField(
        _("Fase TI"), max_length=100,
        blank=True,
        null=True
    )

    ds_modalidade = models.CharField(
        _("Modalidade TI"), max_length=100,
        blank=True,
        null=True
    )

    ds_reestudo_ti = models.CharField(
        _("Reestudo TI"), max_length=80,
        blank=True,
        null=True
    )

    ds_cr = models.CharField(
        max_length=100,         blank=True,
        null=True
    )

    co_cr = models.ForeignKey(
        CoordenacaoRegional,
        to_field='co_cr',
        related_name='terras_indigenas',
        on_delete=models.DO_NOTHING,
        db_column='co_cr',
        db_constraint=False
    )

    no_municipio = models.TextField(
        blank=True,
        null=True
    )

    sg_uf = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )

    st_faixa_fronteira = models.CharField(
        max_length=3,
        blank=True,
        null=True
    )
    dt_em_estudo = models.DateField(
        blank=True,
        null=True
    )

    ds_portaria_em_estudo = models.TextField(
        blank=True,
        null=True
    )

    dt_delimitada = models.DateField(
        blank=True,
        null=True
    )

    ds_despacho_delimitada = models.TextField(
        blank=True,
        null=True
    )

    dt_declarada = models.DateField(
        blank=True,
        null=True
    )

    ds_portaria_declarada = models.TextField(
        blank=True,
        null=True
    )

    dt_homologada = models.DateField(
        blank=True,
        null=True
    )

    ds_decreto_homologada = models.TextField(
        blank=True,
        null=True
    )

    dt_regularizada = models.DateField(
        blank=True,
        null=True
    )

    ds_matricula_regularizada = models.TextField(
        blank=True,
        null=True
    )

    ds_doc_resumo_em_estudo = models.TextField(
        blank=True,
        null=True
    )

    ds_doc_resumo_delimitada = models.TextField(
        blank=True,
        null=True
    )

    ds_doc_resumo_declarada = models.TextField(
        blank=True,
        null=True
    )

    ds_doc_resumo_homologada = models.TextField(
        blank=True,
        null=True
    )

    ds_doc_resumo_regularizada = models.TextField(
        blank=True,
        null=True
    )

    # st_amazonia_legal = models.BooleanField(blank=True,
    #                                         null=True)
    nu_area_ha = models.DecimalField(
        max_digits=100, decimal_places=2,
        blank=True,
        null=True
    )
    dt_cadastro = models.DateTimeField(
        blank=True,
        null=True
    )

    possui_ig = models.BooleanField(
        default=False
    )

    def __str__(self):
        return str(self.no_ti)

    class Meta:
        """Metaclass to `funai.LimiteTerraIndigena`."""
        app_label = 'funai'
        verbose_name = _('Terra Indigena')
        verbose_name_plural = _('Terras Indigenas')
        ordering = ('no_ti', )
        db_table = 'funai\".\"lim_terra_indigena_a'
        managed = False


class ManagementInstrument(models.Model):
    """Instrumental Indigenous Lands model data.

    * Association:
        * Has one: `funai.LimiteTerraIndigena`
    """

    co_funai = models.IntegerField(
        _('Cod Funai'),
        blank=False,
        null=False
    )
    no_ti = models.TextField(
        _('Terras Indígena'),
        blank=True,
        null=False
    )
    no_regiao = models.TextField(
        _('Região'),
        blank=True,
        null=False
    )
    sg_uf = models.TextField(
        _('UF'),
        blank=True,
        null=False
    )
    no_povo = models.TextField(
        _('Povos'),
        blank=True,
        null=False
    )
    no_bioma = models.TextField(
        _('Bioma'),
        blank=True,
        null=False
    )
    ds_parceiros = models.TextField(
        _('Parceiros'),
        blank=True,
        null=False
    )
    cr_funai = models.TextField(
        _('Nome Funai'),
        blank=True,
        null=False
    )
    no_ig = models.TextField(
        _('Instrumento'),
        blank=True,
        null=False
    )
    ds_status = models.TextField(
        _('Status'),
        blank=True,
        null=False
    )
    nu_ano_elaboracao = models.TextField(
        _('Elaborado em'),
        blank=True,
        null=False
    )
    ds_disp_meio_local = models.TextField(
        _('Disponível em'),
        blank=True,
        null=False
    )
    ds_ttl_publi = models.TextField(
        _(''),
        blank=True,
        null=False
    )
    ds_obs = models.TextField(
        _('Observação'),
        blank=True,
        null=False
    )
    dt_cadastro = models.DateTimeField(
        _('Data Registro'),
        blank=True,
        null=True,
        default=timezone.now
    )

    class Meta:
        """Metaclass to `funai.ManagementInstrument`."""
        app_label = 'funai'
        verbose_name = _('Instrumento de Gestão')
        verbose_name_plural = _('Instrumentos de Gestão')
        ordering = ('no_ti',)
        db_table = 'funai\".\"tb_instrumento_gestao_funai'
        managed = False
